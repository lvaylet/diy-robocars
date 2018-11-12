#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helpers import normalize


class TestNormalize:

    def test_1496_steering_should_normalize_to_0(self):
        assert normalize(1496, 1000, 1496, 1984) == 0.0

    def test_1000_steering_should_normalize_to_minus_1(self):
        assert normalize(1000, 1000, 1496, 1984) == -1.0

    def test_1984_steering_should_normalize_to_plus_1(self):
        assert normalize(1984, 1000, 1496, 1984) == 1.0
