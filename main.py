from dataclasses import dataclass
from typing import Tuple
import matplotlib.pyplot as pyplot
import numpy


@dataclass
class Square:
    x_min: float = 0.0
    x_max: float = 1.0
    y_min: float = 0.0
    y_max: float = 1.0

    def __init__(
            self,
            scale: float = 1.0,
            translation: Tuple[float, float] = (0.0, 0.0),
    ) -> 'Square':
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
        self.p1 = numpy.array([self.x_min, self.y_min])  # bottom left
        self.p2 = numpy.array([self.x_max, self.y_min])  # bottom right
        self.p3 = numpy.array([self.x_max, self.y_max])  # top right
        self.p4 = numpy.array([self.x_min, self.y_max])  # top left

    def draw_border(
            self,
            axis: pyplot.Axes,
            line_width: float = 1.0,
            line_style: str = "solid",
            marker: str = "",
            color: str = "k") -> None:
        """Draw the borders of the sqaure"""
        points = numpy.stack([self.p1, self.p2, self.p3, self.p4, self.p1])
        axis.plot(
            points[:, 0],
            points[:, 1],
            linewidth=line_width,
            linestyle=line_style,
            marker=marker,
            color=color)

    def distance_to_hit_boundary(
            self, X: numpy.ndarray, Y: numpy.ndarray, angle: float
    ) -> numpy.ndarray:
        """distance from the each point (x, y) given the angle until the
        boundary of the sqaure

        """
        # TODO: this only works for a single angle for all the lines
        #       meaning that if we want to have varying angles withing
        #       one square, it won't work

        # TODO: this isn't very readable, can you simplify or add
        #       description?

        if numpy.cos(angle) == 0:
            distances = self.y_max - Y
        elif numpy.sin(angle) == 0:
            distances = self.x_max - X
        else:
            if 0 <= angle <= numpy.pi/2:
                distances = numpy.stack(
                    [numpy.abs((self.x_max - X) / numpy.cos(angle)),
                     numpy.abs((self.y_max - Y) / numpy.sin(angle))],
                    axis=1).min(axis=1)
            elif -numpy.pi/2 <= angle < 0:
                distances = numpy.stack(
                    [numpy.abs((self.x_max - X) / numpy.cos(angle)),
                     numpy.abs((self.y_min - Y) / numpy.sin(angle))],
                    axis=1).min(axis=1)
            elif numpy.pi/2 < angle <= numpy.pi:
                distances = numpy.stack(
                    [numpy.abs((self.x_min - X) / numpy.cos(angle)),
                     numpy.abs((self.y_max - Y) / numpy.sin(angle))],
                    axis=1).min(axis=1)
            elif -numpy.pi <= angle < -numpy.pi/2:
                distances = numpy.stack(
                    [numpy.abs((self.x_min - X) / numpy.cos(angle)),
                     numpy.abs((self.y_min - Y) / numpy.sin(angle))],
                    axis=1).min(axis=1)
        return distances

    def inside_lines_1(
            self, count: int, angle: float
    ) -> Tuple[numpy.ndarray, numpy.ndarray]:
        """
        * all lines have the same angle
        * the x-y of starting points are uniformly distributed
        * the ending points goes all the way to the border of boundary
        """
        starts_x = numpy.random.uniform(
            low=self.x_min, high=self.x_max, size=count)
        starts_y = numpy.random.uniform(
            low=self.y_min, high=self.y_max, size=count)
        lengths = self.distance_to_hit_boundary(
            starts_x, starts_y, angle)
        ends_x = starts_x + lengths * numpy.cos(angle)
        ends_y = starts_y + lengths * numpy.sin(angle)
        return starts_x, starts_y, ends_x, ends_y

    def draw_inside_lines(
            self,
            axis: pyplot.Axes,
            count: int,
            angle: float,
            line_width: float = 0.5,
            line_style: str = "solid",
            marker: str = "",
            color: str = "k") -> None:
        """"""
        # TODO: Make the drawing function generic an dindependant of
        #       the line drawing
        starts_x, starts_y, ends_x, ends_y = self.inside_lines_1(
            count=count, angle=angle)
        # in order to prevent pyplot from drawing a line in between
        # two points, put a pair of [nan, nan] between them:
        # [[p1x, p1y], [p2x, p2y], [nan, nan], [p3x, p3y],...]
        nans = numpy.empty(count)
        nans.fill(numpy.nan)
        points = numpy.stack(
            [starts_x, starts_y, ends_x, ends_y, nans, nans],
            axis=1).reshape((count*3, 2))
        axis.plot(
            points[:, 0],
            points[:, 1],
            linewidth=line_width,
            linestyle=line_style,
            marker=marker,
            color=color)


def normalize(
        value: float, interval: Tuple[float, float]) -> float:
    """given a value from the interval, normalize it to [0, 1]

    it is opposit to \"map_to_interval\"
    map_to_interval(normalize(v, (min, max)), (min, max)) == v
    """
    assert interval[0] <= value <= interval[1], "value must be in interval"
    return (value - interval[0]) / (interval[1] - interval[0])


def map_to_interval(
        value: float, interval: Tuple[float, float]) -> float:
    """given a value between [0, 1], map it to the interval

    it is opposite of the \"normalize\"
    map_to_interval(normalize(v, (min, max)), (min, max)) == v
    """
    assert interval[0] <= interval[1], "wrong interval"
    assert 0 <= value <= 1, "value must be in [0, 1]"
    return value * (interval[1] - interval[0]) + interval[0]


# TODO: turn the big picture drawing (examples) into functions

if 0:  # examples_1
    figure, axis = pyplot.subplots(
        nrows=1, ncols=1, sharex=True, figsize=(10, 10))
    x_range = (0, 20)
    y_range = (0, 20)
    distance_to_origin_range = (
        numpy.sqrt(x_range[0]**2 + y_range[0]**2),
        numpy.sqrt(x_range[1]**2 + y_range[1]**2),
    )
    count_range = (0, 150)
    for x in range(*x_range):
        for y in range(*y_range):
            distance_to_origin = numpy.sqrt(x**2 + y**2)
            count_normalized = normalize(
                value=distance_to_origin, interval=distance_to_origin_range)
            count = int(map_to_interval(
                value=count_normalized, interval=count_range))
            angle = numpy.arctan2(y, x)
            if (x == 0 and y == 0):
                angle = numpy.deg2rad(45)
            square = Square(translation=(x, y))
            square.draw_border(axis=axis)
            square.draw_inside_lines(axis=axis,
                                     count=count,
                                     angle=angle)
    pyplot.axis("equal")
    pyplot.axis('off')
    pyplot.tight_layout()
    pyplot.show()

if 0:  # examples_2
    figure, axis = pyplot.subplots(
        nrows=1, ncols=1, sharex=True, figsize=(10, 10))
    x_range = (0, 5)
    y_range = (0, 5)
    distance_to_origin_range = (
        numpy.sqrt(x_range[0]**2 + y_range[0]**2),
        numpy.sqrt(x_range[1]**2 + y_range[1]**2),
    )
    count_range = (0, 150)
    for x in range(*x_range):
        for y in range(*y_range):
            if x == y == 0:
                continue
            distance_to_origin = numpy.sqrt(x**2 + y**2)
            count_normalized = normalize(
                value=distance_to_origin, interval=distance_to_origin_range)
            count = int(map_to_interval(
                value=count_normalized, interval=count_range))
            angle = numpy.arctan2(y, x)
            if (x == 0 and y == 0):
                angle = numpy.deg2rad(45)
            square = Square(
                scale=(1/(distance_to_origin+0.2)), translation=(x, y))
            square.draw_border(axis=axis)
            square.draw_inside_lines(axis=axis,
                                     count=count,
                                     angle=angle)
    pyplot.axis("equal")
    pyplot.axis('off')
    pyplot.tight_layout()
    pyplot.show()

if 0:  # examples_3
    figure, axis = pyplot.subplots(
        nrows=1, ncols=1, sharex=True, figsize=(10, 10))
    x_range = (0, 10)
    y_range = (0, 10)
    distance_to_origin_range = (
        numpy.sqrt(x_range[0]**2 + y_range[0]**2),
        numpy.sqrt(x_range[1]**2 + y_range[1]**2),
    )
    count_range = (0, 100)
    for x in range(*x_range):
        for y in range(*y_range):
            if x == y == 0:
                continue
            distance_to_origin = numpy.sqrt(x**2 + y**2)
            count_normalized = normalize(
                value=distance_to_origin, interval=distance_to_origin_range)
            count = int(map_to_interval(
                value=count_normalized, interval=count_range))
            angle = numpy.arctan2(y, x)
            if (x == 0 and y == 0):
                angle = numpy.deg2rad(45)
            square.draw_border(axis=axis)
            square.draw_inside_lines(axis=axis,
                                     count=count,
                                     angle=angle)
    pyplot.axis("equal")
    pyplot.axis('off')
    pyplot.tight_layout()
    pyplot.show()

if 0:  # examples_4
    figure, axis = pyplot.subplots(
        nrows=1, ncols=1, sharex=True, figsize=(10, 10))
    x_range = (-9, 10)
    y_range = (-9, 10)
    distance_to_origin_range = (
        0,  # numpy.sqrt(x_range[0]**2 + y_range[0]**2),
        numpy.sqrt(x_range[1]**2 + y_range[1]**2),
    )
    count_range = (0, 150)
    for x in range(*x_range):
        for y in range(*y_range):
            distance_to_origin = numpy.sqrt(x**2 + y**2)
            count_normalized = normalize(
                value=distance_to_origin, interval=distance_to_origin_range)
            count = int(map_to_interval(
                value=count_normalized, interval=count_range))
            # count = 50
            angle = numpy.arctan2(y, x)
            if (x == 0 and y == 0):
                count = 0
                angle = numpy.deg2rad(45)
            square = Square(translation=(x, y))
            square.draw_border(axis=axis)
            square.draw_inside_lines(axis=axis,
                                     count=count,
                                     angle=angle)
    pyplot.axis("equal")
    pyplot.axis('off')
    pyplot.tight_layout()
    pyplot.show()

# TODO: an interactive mode where the "origin" shifts with the mouse curser
