from typing import Tuple, Callable
import matplotlib.pyplot as plt
import numpy as np
from common import normalize, map_to_interval


class Square:
    x_min: float = 0.0
    x_max: float = 1.0
    y_min: float = 0.0
    y_max: float = 1.0

    def __init__(
        self,
        scale: float = 1.0,
        translation: Tuple[float, float] = (0.0, 0.0),
    ) -> "Square":
        self.resize(scale=scale)
        self.translate(translation=translation)
        self.set_corners()

    def resize(self, scale: float) -> None:
        """resize the square according to input scale"""
        self.x_min *= scale
        self.x_max *= scale
        self.y_min *= scale
        self.y_max *= scale
        self.set_corners()

    def translate(self, translation: Tuple[float, float]) -> None:
        """translate the square according to input scale"""
        self.x_min += translation[0]
        self.x_max += translation[0]
        self.y_min += translation[1]
        self.y_max += translation[1]
        self.set_corners()

    def set_corners(self) -> None:
        """set values for four points representing the corners of the square"""
        self.p1 = np.array([self.x_min, self.y_min])  # bottom left
        self.p2 = np.array([self.x_max, self.y_min])  # bottom right
        self.p3 = np.array([self.x_max, self.y_max])  # top right
        self.p4 = np.array([self.x_min, self.y_max])  # top left

    def draw_border(
        self,
        axis: plt.Axes,
        line_width: float = 1.0,
        line_style: str = "solid",
        marker: str = "",
        color: str = "k",
    ) -> None:
        """Draw the borders of the square"""
        points = np.stack([self.p1, self.p2, self.p3, self.p4, self.p1])
        axis.plot(
            points[:, 0],
            points[:, 1],
            linewidth=line_width,
            linestyle=line_style,
            marker=marker,
            color=color,
        )

    def inside_lines(self, count: int, angle: float) -> np.ndarray:
        """
        * all lines have the same angle
        * the x-y of starting points are uniformly distributed
        * the ending points goes all the way to the border of boundary
        """
        # Get random starting points for inside lines
        starts_x = np.random.uniform(low=self.x_min, high=self.x_max, size=count)
        starts_y = np.random.uniform(low=self.y_min, high=self.y_max, size=count)

        # Calculate the length of each line until it hits a boundary
        if np.cos(angle) >= 0:
            border_x = self.x_max  # angle shooting to the right
        else:
            border_x = self.x_min  # angle shooting to the left
        if np.sin(angle) >= 0:
            border_y = self.y_max  # angle shooting up
        else:
            border_y = self.y_min  # angle shooting down
        #  we don't have to worry about division by zero when cos(angle)
        #  or sin(angle) are zero, because they can only shoot up to
        #  +inf and we are interested in min values
        lengths = np.stack(
            [
                np.abs((border_x - starts_x) / np.cos(angle)),
                np.abs((border_y - starts_y) / np.sin(angle)),
            ],
            axis=1,
        ).min(axis=1)

        # Compute the ending point of each line
        ends_x = starts_x + lengths * np.cos(angle)
        ends_y = starts_y + lengths * np.sin(angle)

        # in order to prevent plt from drawing a line in between
        # two points, put a pair of [nan, nan] between them:
        # [[p1x, p1y], [p2x, p2y], [nan, nan], [p3x, p3y],...]
        nans = np.empty(count)
        nans.fill(np.nan)
        points = np.stack(
            [starts_x, starts_y, ends_x, ends_y, nans, nans], axis=1
        ).reshape((count * 3, 2))
        return points


def draw(
    x_range: Tuple[int, int],
    y_range: Tuple[int, int],
    count_range: Tuple[int, int],
    get_distance_to_origin_range: Callable,
    scale: Callable,
    translation: Callable,
) -> None:
    distance_to_origin_range = get_distance_to_origin_range(x_range, y_range)
    figure, axis = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(10, 10))
    points = list()
    for x in range(*x_range):
        for y in range(*y_range):
            distance_to_origin = np.sqrt(x**2 + y**2)
            count_normalized = normalize(
                value=distance_to_origin, interval=distance_to_origin_range
            )
            count = int(map_to_interval(value=count_normalized, interval=count_range))
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


def get_distance_to_origin_range(
    x_range: Tuple[int, int], y_range: Tuple[int, int]
) -> Tuple[int, int]:
    return (
        np.sqrt(x_range[0] ** 2 + y_range[0] ** 2),
        np.sqrt(x_range[1] ** 2 + y_range[1] ** 2),
    )


#  # example 1
draw(
    x_range=(0, 20),
    y_range=(0, 20),
    count_range=(0, 150),
    get_distance_to_origin_range=get_distance_to_origin_range,
    scale=lambda x, y: 1,
    translation=lambda x, y: (x, y),
)


#  # examples 2
draw(
    x_range=(0, 5),
    y_range=(0, 5),
    count_range=(0, 150),
    get_distance_to_origin_range=get_distance_to_origin_range,
    scale=lambda x, y: 1 / (np.sqrt(x**2 + y**2) + 0.2),
    translation=lambda x, y: (x, y),
)


#  # examples 3 -- this was the one that did not draw grid
draw(
    x_range=(0, 10),
    y_range=(0, 10),
    count_range=(0, 100),
    get_distance_to_origin_range=get_distance_to_origin_range,
    scale=lambda x, y: 1,
    translation=lambda x, y: (x, y),
)


#  # examples 4
def get_distance_to_origin_range(
    x_range: Tuple[int, int], y_range: Tuple[int, int]
) -> Tuple[int, int]:
    return (
        0,
        np.sqrt(np.abs(x_range).max() ** 2 + np.abs(y_range).max() ** 2),
    )


draw(
    x_range=(-9, 10),
    y_range=(-9, 10),
    count_range=(0, 150),
    get_distance_to_origin_range=get_distance_to_origin_range,
    scale=lambda x, y: 1,
    translation=lambda x, y: (x, y),
)
