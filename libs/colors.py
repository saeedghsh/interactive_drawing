"""Colors"""

import argparse
from typing import NamedTuple, Tuple


class Color(NamedTuple):  # pylint: disable=missing-class-docstring
    red: int
    green: int
    blue: int


BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)


def parse_color(value: str) -> Tuple[int, int, int]:
    """Parse a string into a tuple of three integers. Example input: "255,255,255" """
    try:
        parts = value.split(",")
        return tuple(int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Color must be a comma-separated list of three integers (e.g., 255,255,255)."
        ) from exc
