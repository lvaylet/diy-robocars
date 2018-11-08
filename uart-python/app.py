#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read data from Arduino over serial port.
"""

import logging

import serial

logging.basicConfig(level=logging.DEBUG)

ser = serial.Serial('/dev/ttyACM0', 57600)

logging.info('Connected to /dev/ttyACM0.')
logging.info('Reading data received on /dev/ttyACM0, press Ctrl-C to quit...')
while True:
    ser.readline()
