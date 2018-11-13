#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read RC receiver values over serial port and publish steering/throttle orders to data broker.
"""

import json
import logging
import os

import pika
import serial

import helpers

# region Logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# endregion

# region Serial port

SERIAL_PORT = os.environ.get('SERIAL_PORT', '/dev/ttyACM0')
SERIAL_SPEED_BAUDS = int(os.environ.get('SERIAL_SPEED_BAUDS', '57600'))

ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED_BAUDS)
logger.info('Connected to serial port %s at %d bauds.', SERIAL_PORT, SERIAL_SPEED_BAUDS)

# endregion

# region Data broker (RabbitMQ)

RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'guest')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'guest')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
RABBITMQ_QUEUE = os.environ.get('RABBITMQ_QUEUE', 'steering_and_throttle')

credentials = pika.PlainCredentials(username=RABBITMQ_USERNAME,
                                    password=RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,
                                       port=RABBITMQ_PORT,
                                       virtual_host='/',
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue=RABBITMQ_QUEUE)

# With topics:
# channel.exchange_declare(exchange='topic_rc_receiver_pulse_widths_microseconds',
#                          exchange_type='topic')

# endregion

STEERING_CENTER = os.environ.get('STEERING_CENTER', 1500)
STEERING_MIN = os.environ.get('STEERING_MIN', 1000)
STEERING_MAX = os.environ.get('STEERING_MAX', 2000)
THROTTLE_CENTER = os.environ.get('STEERING_CENTER', 1500)
THROTTLE_MIN = os.environ.get('STEERING_MIN', 1000)
THROTTLE_MAX = os.environ.get('STEERING_MAX', 2000)

logger.info('Reading data from serial port. Press CTRL+C to exit.')
while True:
    data_byte_array = ser.readline()
    data_dict = helpers.serial_data_to_dict(data_byte_array)
    try:
        steering = data_dict['CH1']
        throttle = data_dict['CH2']
        steering_normalized = helpers.normalize(reading=steering,
                                                min_reading=STEERING_MIN,
                                                center_reading=STEERING_CENTER,
                                                max_reading=STEERING_MAX)
        throttle_normalized = helpers.normalize(reading=throttle,
                                                min_reading=THROTTLE_MIN,
                                                center_reading=THROTTLE_CENTER,
                                                max_reading=THROTTLE_MAX)
        payload = {
            'steering': steering_normalized,
            'throttle': throttle_normalized,
        }
        channel.basic_publish(exchange='',
                              routing_key='steering_and_throttle',
                              body=json.dumps(payload))
        # With topics:
        # channel.basic_publish(exchange='topic_rc_receiver_pulse_widths_microseconds',
        #                       routing_key=routing_key,  # TO BE DEFINED
        #                       body=json.dumps(payload))
    except KeyError as e:
        # `CH1` or `CH2` are not in `data_dict`
        logger.error('Could not find key [%s] in data_dict.', e.args[0])
