#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helpers import pulse_width_microseconds_to_ticks


def test_0_microseconds_should_be_0_ticks_at_50_hz():
    assert pulse_width_microseconds_to_ticks(0, 50) == 0


def test_0_microseconds_should_be_0_ticks_at_1000_hz():
    assert pulse_width_microseconds_to_ticks(0, 1000) == 0


def test_20000_microseconds_should_be_4096_ticks_at_50_hz():
    assert pulse_width_microseconds_to_ticks(20000, 50) == 4096


def test_10_microseconds_should_be_40_ticks_at_1000_hz():
    assert pulse_width_microseconds_to_ticks(10, 1000) == 40


def test_1000_microseconds_should_be_204_ticks_at_1000_hz():
    assert pulse_width_microseconds_to_ticks(1000, 50) == 204


def test_1500_microseconds_should_be_307_ticks_at_1000_hz():
    assert pulse_width_microseconds_to_ticks(1500, 50) == 307


def test_2000_microseconds_should_be_409_ticks_at_50_hz():
    assert pulse_width_microseconds_to_ticks(2000, 50) == 409
