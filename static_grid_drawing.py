from typing import Tuple, Callable
import matplotlib.pyplot as plt
import numpy as np

from libs.common import normalize_to_unit_interval, scale_to_custom_interval
from libs.square import Square


def _draw(
    x_range: Tuple[int, int],
    y_range: Tuple[int, int],
    count_range: Tuple[int, int],
    distance_to_origin_range: Callable,
    scale: Callable,
    translation: Callable,
) -> None:
    distance_to_origin_range = distance_to_origin_range(x_range, y_range)
    _, axis = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(10, 10))
    points = list()
    for x in range(*x_range):
        for y in range(*y_range):
            distance_to_origin = np.sqrt(x**2 + y**2)
            count_normalized = normalize_to_unit_interval(
                values=distance_to_origin, interval=distance_to_origin_range
            )
            count = int(
                scale_to_custom_interval(values=count_normalized, interval=count_range)
            )
            angle = np.arctan2(y, x)
            square = Square(scale=scale(x, y), translation=translation(x, y))
            points += [
                square.inside_lines(count, angle),
                np.array([[np.nan, np.nan]]),
            ]
            square.draw_border(axis=axis)
    points = np.concatenate(points)
    axis.plot(
        points[:, 0],
        points[:, 1],
        linewidth=0.5,
        linestyle="solid",
        marker="",
        color="k",
    )
    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def _get_distance_to_origin_range(
    x_range: Tuple[int, int], y_range: Tuple[int, int]
) -> Tuple[int, int]:
    return (
        np.sqrt(x_range[0] ** 2 + y_range[0] ** 2),
        np.sqrt(x_range[1] ** 2 + y_range[1] ** 2),
    )


#  # example 1
_draw(
    x_range=(0, 20),
    y_range=(0, 20),
    count_range=(0, 150),
    distance_to_origin_range=_get_distance_to_origin_range,
    scale=lambda x, y: 1,
    translation=lambda x, y: (x, y),
)


#  # examples 2
_draw(
    x_range=(0, 5),
    y_range=(0, 5),
    count_range=(0, 150),
    distance_to_origin_range=_get_distance_to_origin_range,
    scale=lambda x, y: 1 / (np.sqrt(x**2 + y**2) + 0.2),
    translation=lambda x, y: (x, y),
)


#  # examples 3 -- this was the one that did not draw grid
_draw(
    x_range=(0, 10),
    y_range=(0, 10),
    count_range=(0, 100),
    distance_to_origin_range=_get_distance_to_origin_range,
    scale=lambda x, y: 1,
    translation=lambda x, y: (x, y),
)


#  # examples 4
def _get_distance_to_origin_range(
    x_range: Tuple[int, int], y_range: Tuple[int, int]
) -> Tuple[int, int]:
    return (
        0,
        np.sqrt(np.abs(x_range).max() ** 2 + np.abs(y_range).max() ** 2),
    )


_draw(
    x_range=(-9, 10),
    y_range=(-9, 10),
    count_range=(0, 150),
    distance_to_origin_range=_get_distance_to_origin_range,
    scale=lambda x, y: 1,
    translation=lambda x, y: (x, y),
)
