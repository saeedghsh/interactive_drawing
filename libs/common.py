"""Utils to scale values from [0,1] to custom interval and vise versa"""

from typing import Tuple

import numpy


def normalize_to_unit_interval(
    values: numpy.ndarray, interval: Tuple[float, float]
) -> numpy.ndarray:
    """Return values normalized to [0, 1] according to the interval"""
    if interval[0] >= interval[1]:
        raise ValueError(f"wrong interval {interval}")
    if (interval[0] > values).any() or (values > interval[1]).any():
        raise ValueError("values out of interval")
    return (values - interval[0]) / (interval[1] - interval[0])


def scale_to_custom_interval(
    values: numpy.ndarray, interval: Tuple[float, float]
) -> numpy.ndarray:
    """Return values scaled to the interval"""
    if interval[0] >= interval[1]:
        raise ValueError(f"wrong interval {interval}")
    if (0 > values).any() or (values > 1).any():
        raise ValueError("values out of [0, 1]")
    return values * (interval[1] - interval[0]) + interval[0]
