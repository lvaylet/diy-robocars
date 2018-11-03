#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


def pulse_width_microseconds_to_ticks(desired_pulse_width_microseconds: int, pwm_freq_hz: int = 50) -> int:
    """
    Convert a PWM pulse width from microseconds to 12-bit ticks (0..4095).

    If setting the pulse width in microseconds is easier, you can do that by first figuring out how long each cycle is.
    That would be 1/pwm_freq_hz. For 1000 Hz, that would be 1 millisecond. For 50 Hz, that would be 20 milliseconds.
    Then divide by 4096 to get the time per tick. That would be 1 millisecond / 4096 = ~0.24 microseconds at 1000 Hz, or
    20 milliseconds / 4096 = ~4.88 microseconds at 50 Hz. If you want a pulse that is 10 microseconds long, divide the
    time by time-per-tick (10 us / 0.24 us = 42). Then turn on at tick 0 and turn off at tick 42.

    Reference: https://cdn-learn.adafruit.com/downloads/pdf/adafruit-16-channel-servo-driver-with-raspberry-pi.pdf

    :param desired_pulse_width_microseconds: The pulse width to convert, in microseconds
    :type desired_pulse_width_microseconds: int
    :param pwm_freq_hz: The PWM frequency
    :type pwm_freq_hz: int
    :return: The pulse width in ticks with 12-bit resolution (0..4095)
    :rtype: int
    """
    microseconds_per_second = 1_000_000
    microseconds_per_period = microseconds_per_second // pwm_freq_hz
    logger.debug('There are %d microseconds per period at %d Hz', microseconds_per_period, pwm_freq_hz)
    microseconds_per_tick = microseconds_per_period / 4096  # 12-bit resolution spans 2^12 = 4096 ticks
    logger.debug('One tick represents %.2f microseconds', microseconds_per_tick)
    pulse_width_ticks = int(desired_pulse_width_microseconds // microseconds_per_tick)
    return pulse_width_ticks
