#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use the Adafruit PCA9685 PWM controller library to steer the wheels of the RC car from left to right.
"""

import logging
import os
import time

import Adafruit_PCA9685
import serial

import helpers

# region Logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# endregion

# region Constants

PWM_FREQUENCY_HZ = int(os.environ.get('PWN_FREQUENCY_HZ', '50'))  # 50 Hz is suitable for most servos with 20 ms frames

STEERING_RIGHT_PULSE_LENGTH_MICROSECONDS = int(os.environ.get('STEERING_MIN', '1000'))
STEERING_LEFT_PULSE_WIDTH_MICROSECONDS = int(os.environ.get('STEERING_MAX', '1984'))
STEERING_CENTER_PULSE_WIDTH_MICROSECONDS = int(os.environ.get('STEERING_CENTER', '1984'))

THROTTLE_RIGHT_PULSE_LENGTH_MICROSECONDS = int(os.environ.get('THROTTLE_MIN', '1000'))
THROTTLE_LEFT_PULSE_WIDTH_MICROSECONDS = int(os.environ.get('THROTTLE_MAX', '1984'))
THROTTLE_CENTER_PULSE_WIDTH_MICROSECONDS = int(os.environ.get('THROTTLE_CENTER', '1984'))

STEERING_CHANNEL_ON_PCA9685 = int(os.environ.get('STEERING_CHANNEL_ON_PCA9685', '0'))
THROTTLE_CHANNEL_ON_PCA9685 = int(os.environ.get('THROTTLE_CHANNEL_ON_PCA9685', '1'))

# endregion

# region Serial port

SERIAL_PORT = os.environ.get('SERIAL_PORT', '/dev/ttyACM0')
SERIAL_SPEED_BAUDS = int(os.environ.get('SERIAL_SPEED_BAUDS', '57600'))

ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED_BAUDS)
logger.info('Connected to serial port %s at %d bauds.', SERIAL_PORT, SERIAL_SPEED_BAUDS)

# endregion

# region PCA9685

logger.info('Connecting to PCA9685...')
pca9685 = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

logger.info('Setting PCA9685 PWM frequency to [%d] Hz...', PWM_FREQUENCY_HZ)
pca9685.set_pwm_freq(PWM_FREQUENCY_HZ)

# endregion

logger.info('Reading data from serial port. Press CTRL+C to exit.')
while True:
    data_byte_array = ser.readline()
    data_dict = helpers.serial_data_to_dict(data_byte_array)
    try:
        steering = data_dict['CH1']
        throttle = data_dict['CH2']
    except KeyError as e:
        # `CH1` or `CH2` are not in `data_dict`
        logger.error('Could not find key [%s] in data_dict.', e.args[0])
        steering = STEERING_CENTER_PULSE_WIDTH_MICROSECONDS
        throttle = THROTTLE_CENTER_PULSE_WIDTH_MICROSECONDS

    pca9685.set_pwm(channel=STEERING_CHANNEL_ON_PCA9685,
                    on=0,
                    off=helpers.pulse_width_microseconds_to_ticks(steering))
    pca9685.set_pwm(channel=THROTTLE_CHANNEL_ON_PCA9685,
                    on=0,
                    off=helpers.pulse_width_microseconds_to_ticks(throttle))
