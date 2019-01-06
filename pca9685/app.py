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

logging_level = logging.DEBUG if 'DEBUG' in os.environ else logging.INFO
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)

# endregion

# region Constants

PWM_FREQUENCY_HZ = int(os.environ.get('PWN_FREQUENCY_HZ', '50'))  # 50 Hz is suitable for most servos with 20 ms frames

STEERING_MIN = int(os.environ.get('STEERING_MIN', '1000'))
STEERING_MAX = int(os.environ.get('STEERING_MAX', '1984'))
STEERING_CENTER = int(os.environ.get('STEERING_CENTER', '1496'))

THROTTLE_MIN = int(os.environ.get('THROTTLE_MIN', '1040'))
THROTTLE_MAX = int(os.environ.get('THROTTLE_MAX', '1996'))
THROTTLE_CENTER = int(os.environ.get('THROTTLE_CENTER', '1532'))

STEERING_LIMIT = float(os.environ.get('STEERING_LIMIT', '1.0'))
THROTTLE_LIMIT = float(os.environ.get('THROTTLE_LIMIT', '0.1'))  # limit throttle to 10% by default

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
    # Read serial data
    data_byte_array = ser.readline()

    # Extract steering and throttle setpoints from serial data
    data_dict = helpers.serial_data_to_dict(data_byte_array)
    try:
        steering = data_dict['CH1']
        throttle = data_dict['CH2']
    except KeyError as e:
        # `CH1` or `CH2` are not in `data_dict`
        logger.error('Could not find key [%s] in data_dict.', e.args[0])
        steering = STEERING_CENTER
        throttle = THROTTLE_CENTER

    logger.debug('Steering = %d, Throttle = %d', steering, throttle)

    # Normalize steering and throttle setpoints to [-1.0; +1.0]
    steering_normalized = helpers.microseconds_to_normalized(steering,
                                                             min_reading=STEERING_MIN,
                                                             center_reading=STEERING_CENTER,
                                                             max_reading=STEERING_MAX)
    throttle_normalized = helpers.microseconds_to_normalized(throttle,
                                                             min_reading=THROTTLE_MIN,
                                                             center_reading=THROTTLE_CENTER,
                                                             max_reading=THROTTLE_MAX)

    logger.debug('Steering normalized = %d, Throttle normalized = %d', steering_normalized, throttle_normalized)

    # Limit steering and throttle normalized setpoints
    if steering_normalized > STEERING_LIMIT:
        steering_normalized_limited = STEERING_LIMIT
    elif steering_normalized < -STEERING_LIMIT:
        steering_normalized_limited = -STEERING_LIMIT
    else:
        steering_normalized_limited = steering_normalized

    if throttle_normalized > THROTTLE_LIMIT:
        throttle_normalized_limited = THROTTLE_LIMIT
    elif throttle_normalized < -THROTTLE_LIMIT:
        throttle_normalized_limited = -THROTTLE_LIMIT
    else:
        throttle_normalized_limited = throttle_normalized

    logger.debug('Steering normalized limited = %d, Throttle normalized limited = %d',
                 steering_normalized_limited,
                 throttle_normalized_limited)

    # Convert normalized and limited setpoints back to pulse widths (in microseconds)
    steering_limited = helpers.normalized_to_microseconds(steering_normalized_limited,
                                                          low=STEERING_MIN,
                                                          center=STEERING_CENTER,
                                                          high=STEERING_MAX)
    throttle_limited = helpers.normalized_to_microseconds(throttle_normalized_limited,
                                                          low=THROTTLE_MIN,
                                                          center=THROTTLE_CENTER,
                                                          high=THROTTLE_MAX)

    logger.debug('Steering limited = %d, Throttle limited = %d', steering_limited, throttle_limited)

    # Apply steering and throttle setpoints
    pca9685.set_pwm(channel=STEERING_CHANNEL_ON_PCA9685,
                    on=0,
                    off=helpers.pulse_width_microseconds_to_ticks(steering_limited))
    pca9685.set_pwm(channel=THROTTLE_CHANNEL_ON_PCA9685,
                    on=0,
                    off=helpers.pulse_width_microseconds_to_ticks(throttle_limited))
