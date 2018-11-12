#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


def normalize(reading: int, min_reading: int, center_reading: int, max_reading: int) -> float:
    """
    Normalizes a reading between -1.0 and 1.0.
    
    Positive and negative values are computed separately, as they can span different intervals initially.
    
    :param reading: The reading to normalize.
    :param min_reading: The minimum reading, mapped to -1.0.
    :param center_reading: The center reading, at rest, mapped to 0.0.
    :param max_reading: The maximum reading, mapped to 1.0.
    :return: The normalized value.
    :type reading: int
    :type min_reading: int
    :type center_reading: int
    :type max_reading: int
    :rtype: float
    """
    centered_reading = reading - center_reading
    if centered_reading > 0:
        normalized_reading = centered_reading / (max_reading - center_reading)
    else:
        normalized_reading = centered_reading / (center_reading - min_reading)

    return normalized_reading
