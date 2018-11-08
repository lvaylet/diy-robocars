#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read data from Arduino over serial port.
"""

import logging
import re

import serial

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ser = serial.Serial('/dev/ttyACM0', 57600)

# Compile a regex that can parse a byte array buffer with an arbitrary number
# of records, each consisting of a channel name, a colon and a numeric value.
SERIAL_DATA_PATTERN = re.compile(b'(CH\d+):(\d+)')


def serial_data_to_dict(byte_array):
    """
    Convert a byte array to a dictionary like {channel name: value}

    :param byte_array: The byte array read from the serial port.
    :type byte_array: bytearray
    :return: The dictionary.
    :rtype: dict[str, int]
    """
    # Parse byte array with regex, as a list of tuples (channel name, value)
    packed = SERIAL_DATA_PATTERN.findall(byte_array)
    # Unpack as a list of tuples
    unpacked = [(x[0].decode(), int(x[1].decode())) for x in packed]
    # Build a dictionary out of the unpacked list of tuples (key = channel name, value = channel value)
    return dict(unpacked)


logger.info('Connected to /dev/ttyACM0.')
logger.info('Reading data received on /dev/ttyACM0, press Ctrl-C to quit...')
while True:
    data_byte_array = ser.readline()
    data_dict = serial_data_to_dict(data_byte_array)
    try:
        logger.info('Steering: %d, Throttle: %d', data_dict['CH1'], data_dict['CH2'])
    except KeyError as e:
        logger.error('KeyError: %s', e.args[0])
