from typing import Tuple
import matplotlib.pyplot as pyplot
import numpy
import common


def lines_in_grid_cells(
    center: Tuple[int, int] = (0, 0),
    x_range: Tuple[int, int] = (-4, 5),
    y_range: Tuple[int, int] = (-4, 5),
    count_range: Tuple[int, int] = (0, 150),
) -> None:
    grid_width = x_range[1] - x_range[0]
    grid_height = y_range[1] - y_range[0]

    # Translation of each grid cell.
    cells_tx, cells_ty = numpy.meshgrid(numpy.arange(*x_range), numpy.arange(*y_range))
    cells_tx = cells_tx.flatten()
    cells_ty = cells_ty.flatten()

    # Compute the line counts per grid cell.
    distance_to_center_range = (
        0,
        numpy.sqrt(grid_width ** 2 + grid_height ** 2),
    )
    distance_to_center = numpy.sqrt(
        (cells_tx - center[0]) ** 2 + (cells_ty - center[1]) ** 2
    )
    count_normalized = common.normalize(
        value=distance_to_center,
        interval=distance_to_center_range,
    )
    counts = common.map_to_interval(
        value=count_normalized,
        interval=count_range,
    ).astype(int)

    # Compute the angle of lines for each grid cell.
    angles = numpy.arctan2(cells_ty - center[1], cells_tx - center[0])

    # Get random starting points for all the lines in all the cells.
    start_points_x = numpy.random.uniform(low=0, high=1, size=counts.sum())
    start_points_y = numpy.random.uniform(low=0, high=1, size=counts.sum())

    # Set the boundaries for the grid cell. At the begining, keep all
    # the grid cells at the same position. Will move the end result
    # instead.
    cells_x_min = numpy.zeros(grid_width * grid_height).repeat(counts)
    cells_x_max = numpy.ones(grid_width * grid_height).repeat(counts)
    cells_y_min = numpy.zeros(grid_width * grid_height).repeat(counts)
    cells_y_max = numpy.ones(grid_width * grid_height).repeat(counts)

    cells_tx = cells_tx.repeat(counts)
    cells_ty = cells_ty.repeat(counts)
    angles = angles.repeat(counts)

    # Calculate the length of each line until it hits a boundary.
    # To that end, first figure out which border each line is going to hit.
    border_x = numpy.where(numpy.cos(angles) >= 0, cells_x_max, cells_x_min)
    border_y = numpy.where(numpy.sin(angles) >= 0, cells_y_max, cells_y_min)
    #  We don't have to worry about divion by zero when cos(angle)
    #  or sin(angle) are zero, because they can only shoot up to
    #  +inf and we are interested in min values.
    lengths = numpy.stack(
        [
            numpy.abs((border_x - start_points_x) / numpy.cos(angles)),
            numpy.abs((border_y - start_points_y) / numpy.sin(angles)),
        ],
        axis=1,
    ).min(axis=1)

    # Compute the ending point of each line.
    end_points_x = start_points_x + lengths * numpy.cos(angles)
    end_points_y = start_points_y + lengths * numpy.sin(angles)

    # Translate lines accroding to the grid cell they belong to.
    start_points_x += cells_tx
    start_points_y += cells_ty
    end_points_x += cells_tx
    end_points_y += cells_ty

    # Compile points to return.
    # Insert NaNs in between points. in order to prevent pyplot from
    # drawing a line in between two points, put a pair of [nan, nan]
    # between them:
    # [[p1x, p1y], [p2x, p2y], [nan, nan], [p3x, p3y],...]
    nans = numpy.full(counts.sum(), numpy.nan)
    points = numpy.stack(
        [
            start_points_x,
            start_points_y,
            end_points_x,
            end_points_y,
            nans,
            nans,
        ],
        axis=1,
    ).reshape((counts.sum() * 3, 2))

    return points


def on_move(event):
    if event.inaxes:
        center = numpy.floor([event.xdata, event.ydata]).astype(int)
        axis = event.inaxes
        axis.cla()  # how the hell can you be the most expensive? :(
        points = lines_in_grid_cells(center=center)
        axis.plot(
            points[:, 0],
            points[:, 1],
            linewidth=0.5,
            linestyle="solid",
            marker="",
            color="k",
        )
        pyplot.axis("equal")
        pyplot.axis("off")
        pyplot.tight_layout()
        figure.canvas.draw_idle()


figure, axis = pyplot.subplots(nrows=1, ncols=1, sharex=True, figsize=(10, 10))
points = lines_in_grid_cells()
axis.plot(
    points[:, 0],
    points[:, 1],
    linewidth=0.5,
    linestyle="solid",
    marker="",
    color="k",
)
pyplot.axis("equal")
pyplot.axis("off")
pyplot.tight_layout()
pyplot.connect("motion_notify_event", on_move)
pyplot.show()
