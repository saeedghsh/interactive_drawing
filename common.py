from typing import Tuple, Union
import numpy


def normalize(
    value: Union[float, numpy.ndarray], interval: Tuple[float, float]
) -> float:
    """given a value from the interval, normalize it to [0, 1]

    it is opposit to \"map_to_interval\"
    map_to_interval(normalize(v, (min, max)), (min, max)) == v
    """
    assert interval[0] <= interval[1], "wrong interval"
    assert (interval[0] <= value).all(), "values must be >= interval[0]"
    assert (value <= interval[1]).all(), "values must be <= interval[1]"
    return (value - interval[0]) / (interval[1] - interval[0])


def map_to_interval(
    value: Union[float, numpy.ndarray], interval: Tuple[float, float]
) -> float:
    """given a value between [0, 1], map it to the interval

    it is opposite of the \"normalize\"
    map_to_interval(normalize(v, (min, max)), (min, max)) == v
    """
    assert interval[0] <= interval[1], "wrong interval"
    assert (0 <= value).all(), "values must be >= 0"
    assert (value <= 1).all(), "values must be <= 1"
    return value * (interval[1] - interval[0]) + interval[0]
