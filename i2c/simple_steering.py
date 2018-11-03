#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use the Adafruit PCA9685 PWM controller library to steer the wheels of the RC car from left to right.
"""

import logging
import time

import Adafruit_PCA9685

from helpers import pulse_width_microseconds_to_ticks

logging.basicConfig(level=logging.DEBUG)

# Initialize the PCA9685 servo shield
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

PWM_FREQUENCY_HZ = 50  # 50 Hz is suitable for most servos, making for 20 ms data frames

# Configure min and max servo pulse lengths, in microseconds
# TODO Map to [1000; 2000] range, or [-1; 1]?
STEERING_RIGHT_PULSE_LENGTH_MICROSECONDS = 1000
STEERING_LEFT_PULSE_WIDTH_MICROSECONDS = 1984
STEERING_IDLE_PULSE_WIDTH_MICROSECONDS = 1496

# The channel your steering motor is connected to on the PCA9685 servo shield
STEERING_CHANNEL = 0

logging.info('Setting PWM frequency to %d Hz...', PWM_FREQUENCY_HZ)
pwm.set_pwm_freq(PWM_FREQUENCY_HZ)

logging.info('IMPORTANT Please secure the RC car before proceeding, for example by putting it on top of a shoebox '
             'or a small but thick book. The wheels should not touch anything.')
input('Press Enter to continue...')

logging.info('Steering wheels, press Ctrl-C to quit...')
while True:
    logging.info('Steering left...')
    pwm.set_pwm(channel=STEERING_CHANNEL,
                on=0,
                off=pulse_width_microseconds_to_ticks(STEERING_LEFT_PULSE_WIDTH_MICROSECONDS))
    time.sleep(1)

    logging.info('Steering right...')
    pwm.set_pwm(channel=STEERING_CHANNEL,
                on=0,
                off=pulse_width_microseconds_to_ticks(STEERING_RIGHT_PULSE_LENGTH_MICROSECONDS))
    time.sleep(1)
