#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use the Adafruit PCA9685 PWM controller library to steer the wheels of the RC car.
"""

import logging
import time

import Adafruit_PCA9685

logging.basicConfig(level=logging.DEBUG)

# Initialize the PCA9685 servo shield
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

# Configure min and max servo pulse lengths
STEERING_MIN_PULSE_LENGTH = 250  # out of 4096
STEERING_MAX_PULSE_LENGTH = 350  # out of 4096

# TODO: Change this value to the channel your motor is connected on ADC.
STEERING_CHANNEL = 0

PULSE_FREQUENCY_HZ = 50  # 50 Hz is suitable for most servos, making for 20 ms data frames
logging.info('Setting PWM frequency to %d Hz...', PULSE_FREQUENCY_HZ)
pwm.set_pwm_freq(PULSE_FREQUENCY_HZ)

logging.info('IMPORTANT Please secure the RC car before proceeding, for example by putting it on top of a shoebox '
             'or a small but thick book...')
input('Press Enter to continue...')

logging.info('Steering wheels, press Ctrl-C to quit...')
while True:

    logging.info('Moving to %d...', STEERING_MIN_PULSE_LENGTH)
    pwm.set_pwm(channel=STEERING_CHANNEL, on=0, off=STEERING_MIN_PULSE_LENGTH)
    time.sleep(1)

    logging.info('Moving to %d...', STEERING_MAX_PULSE_LENGTH)
    pwm.set_pwm(channel=STEERING_CHANNEL, on=0, off=STEERING_MAX_PULSE_LENGTH)
    time.sleep(1)
