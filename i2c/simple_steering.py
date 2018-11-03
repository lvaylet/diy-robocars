#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use the Adafruit PCA9685 PWM controller library to steer the wheels of the RC car from left to right.
"""

import logging
import time

import Adafruit_PCA9685

logging.basicConfig(level=logging.DEBUG)

# Initialize the PCA9685 servo shield
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

PWM_FREQUENCY_HZ = 50  # 50 Hz is suitable for most servos, making for 20 ms data frames

# Configure min and max servo pulse lengths
STEERING_MIN_PULSE_LENGTH = 250  # 0..4095, due to the 12-bit resolution
STEERING_MAX_PULSE_LENGTH = 350  # 0..4095, due to the 12-bit resolution

# The channel your steering motor is connected to on the PCA9685 servo shield
STEERING_CHANNEL = 0


def set_pwm_pulse_in_microseconds(channel: int, pulse: int, pwm_freq_hz: int):
    """
    Set a single PWM channel with a microseconds pulse width.

    If you need to calculate pulse width in microseconds, you can do that by first figuring out how long each cycle is.
    That would be 1/pwm_freq_hz. For 1000 Hz, that would be 1 millisecond. Then divide by 4096 to get the time per tick,
    e.g. 1 millisecond / 4096 = ~0.25 microseconds. If you want a pulse that is 10 microseconds long, divide the time by
    time-per-tick (10us / 0.25 us = 40) then turn on at tick 0 and turn off at tick 40.

    :param channel: The channel that should be updated with the new values (0..15)
    :type channel: int
    :param pulse: The pulse width, in microseconds
    :type pulse: int
    :param pwm_freq_hz: The PWM frequency, in Hz
    :type pwm_freq_hz: int
    """
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= pwm_freq_hz  # how many microseconds per period, given the PWM frequency in Hz?
    logging.debug('{0}us per period', pulse_length)
    pulse_length //= 4096  # 12-bits resolution => 2^12 = 4096 possible values
    logging.debug('{0}us per bit', pulse_length)
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel=channel, on=0, off=pulse)


logging.info('Setting PWM frequency to %d Hz...', PWM_FREQUENCY_HZ)
pwm.set_pwm_freq(PWM_FREQUENCY_HZ)

logging.info('IMPORTANT Please secure the RC car before proceeding, for example by putting it on top of a shoebox '
             'or a small but thick book...')
input('Press Enter to continue...')

logging.info('Steering wheels, press Ctrl-C to quit...')
while True:
    logging.info('Setting pulse width to %d...', STEERING_MIN_PULSE_LENGTH)
    pwm.set_pwm(channel=STEERING_CHANNEL, on=0, off=STEERING_MIN_PULSE_LENGTH)
    time.sleep(1)

    logging.info('Setting pulse width to %d...', STEERING_MAX_PULSE_LENGTH)
    pwm.set_pwm(channel=STEERING_CHANNEL, on=0, off=STEERING_MAX_PULSE_LENGTH)
    time.sleep(1)
