#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helpers import map_to_range, pulse_width_microseconds_to_ticks


class TestMapToRange:

    def test_0_microseconds_should_map_to_0_ticks_at_50_hz(self):
        # Map from [0; 20 ms] to [0; 4095] (20 ms because of 50 Hz)
        assert map_to_range(0, 0, 20000, 0, 4095) == 0

    def test_2_microseconds_should_map_to_0_ticks_at_50_hz(self):
        assert map_to_range(2, 0, 20000, 0, 4095) == 0

    def test_7_microseconds_should_map_to_1_ticks_at_50_hz(self):
        assert map_to_range(7, 0, 20000, 0, 4095) == 1

    def test_20000_microseconds_should_map_to_4095_ticks_at_50_hz(self):
        assert map_to_range(20000, 0, 20000, 0, 4095) == 4095


class TestMicrosecondsToTicks:

    def test_0_microseconds_should_be_0_ticks_at_50_hz(self):
        assert pulse_width_microseconds_to_ticks(0, 50) == 0

    def test_0_microseconds_should_be_0_ticks_at_1000_hz(self):
        assert pulse_width_microseconds_to_ticks(0, 1000) == 0

    def test_20000_microseconds_should_be_4095_ticks_at_50_hz(self):
        assert pulse_width_microseconds_to_ticks(20000, 50) == 4095

    def test_10_microseconds_should_be_40_ticks_at_1000_hz(self):
        assert pulse_width_microseconds_to_ticks(10, 1000) == 40

    def test_1000_microseconds_should_be_204_ticks_at_1000_hz(self):
        assert pulse_width_microseconds_to_ticks(1000, 50) == 204

    def test_1500_microseconds_should_be_307_ticks_at_1000_hz(self):
        assert pulse_width_microseconds_to_ticks(1500, 50) == 307

    def test_2000_microseconds_should_be_409_ticks_at_50_hz(self):
        assert pulse_width_microseconds_to_ticks(2000, 50) == 409
