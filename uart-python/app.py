#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read RC receiver values over serial port and send steering/throttle pulse widths to data broker.
"""

import json
import logging
import os
import re
from typing import Dict

import pika
import serial

# region Logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# endregion

# region Serial port

SERIAL_PORT = os.environ.get('SERIAL_PORT', '/dev/ttyACM0')
SERIAL_SPEED_BAUDS = int(os.environ.get('SERIAL_SPEED_BAUDS', '57600'))
# Compile a regex that can parse a byte array buffer with an arbitrary number
# of records, each consisting of a channel name, a colon and a numeric value.
SERIAL_DATA_PATTERN = re.compile(b'(CH\d+):(\d+)')

ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED_BAUDS)
logger.info('Connected to %s at %d bauds.', SERIAL_PORT, SERIAL_SPEED_BAUDS)

# endregion

# region Data broker (RabbitMQ)

credentials = pika.PlainCredentials(username='guest',
                                    password='guest')
parameters = pika.ConnectionParameters(host='rabbitmq',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='pulse_width_microseconds')


# With topics:
# channel.exchange_declare(exchange='topic_rc_receiver_pulse_widths_microseconds',
#                          exchange_type='topic')


# endregion

# region Helpers

def serial_data_to_dict(byte_array: bytes) -> Dict[str, int]:
    """
    Convert a byte array to a dictionary like {channel name: value}

    :param byte_array: The byte array read from the serial port.
    :type byte_array: bytes
    :return: The dictionary.
    :rtype: dict[str, int]
    """
    # Parse byte array with regex, as a list of tuples (channel name, value)
    packed = SERIAL_DATA_PATTERN.findall(byte_array)
    # Unpack as a list of tuples
    unpacked = [(x[0].decode(), int(x[1].decode())) for x in packed]
    # Build a dictionary out of the unpacked list of tuples (key = channel name, value = channel value)
    return dict(unpacked)


# endregion

logger.info('Reading data from serial port. Press CTRL+C to exit.')
while True:
    data_byte_array = ser.readline()
    data_dict = serial_data_to_dict(data_byte_array)
    try:
        payload = {
            'Steering': data_dict['CH1'],
            'Throttle': data_dict['CH2'],
        }
        # With topics:
        # channel.basic_publish(exchange='topic_rc_receiver_pulse_widths_microseconds',
        #                       routing_key=routing_key,  # TO BE DEFINED
        #                       body=json.dumps(payload))
        channel.basic_publish(exchange='',
                              routing_key='pulse_width_microseconds',
                              body=json.dumps(payload))
    except KeyError as e:
        # CH1 and CH2 could not be found in data_dict
        logger.error('KeyError: %s', e.args[0])
