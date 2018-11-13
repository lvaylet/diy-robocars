#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helpers import normalize, serial_data_to_dict


class TestNormalize:

    def test_1496_steering_should_normalize_to_0(self):
        assert normalize(1496, 1000, 1496, 1984) == 0.0

    def test_1000_steering_should_normalize_to_minus_1(self):
        assert normalize(1000, 1000, 1496, 1984) == -1.0

    def test_1984_steering_should_normalize_to_plus_1(self):
        assert normalize(1984, 1000, 1496, 1984) == 1.0


class TestSerialDataToDict:

    def test_valid_byte_array_should_return_valid_dict(self):
        assert serial_data_to_dict(b'CH1:1400\tCH2:1600\n') == {'CH1': 1400, 'CH2': 1600}
