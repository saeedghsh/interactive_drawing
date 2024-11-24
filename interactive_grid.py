"""Interactive visualization with pygame.

A distribution of line segments that are all aligned towards the mouse position.

Discrete Mode.
"""

# pylint: disable=import-error, no-name-in-module, no-member, c-extension-no-member

from typing import Sequence, Tuple
import argparse
import sys
import numpy as np
import pygame
import pygame.locals
import pygame_gui

from libs.colors import BLACK, WHITE, Color
from libs.utils import print_output


class DrawManager:  # pylint: disable=too-few-public-methods
    """Represents the basis for drawing on the pygame.surface.Surface."""

    def __init__(self, width, height, cell_size, max_lines):
        self._cell_size = cell_size
        self._max_lines = max_lines
        self._rows = height // cell_size
        self._cols = width // cell_size

    @staticmethod
    def _tile_along_axis_2(arr: np.ndarray, count: int) -> np.ndarray:
        return np.tile(arr[:, :, None], (1, 1, count))

    def _anchor_point_xy_to_rc(self, anchor_point: Tuple[int, int]) -> Tuple[int, int]:
        anchor_x, anchor_y = anchor_point
        anchor_row = anchor_y // self._cell_size
        anchor_col = anchor_x // self._cell_size
        return anchor_col, anchor_row

    def _starting_points(
        self, col_indices: np.ndarray, row_indices: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        array_shape_3d = (self._rows, self._cols, self._max_lines)
        cell_x = col_indices * self._cell_size
        cell_y = row_indices * self._cell_size
        cell_x_tiled = self._tile_along_axis_2(cell_x, self._max_lines)
        cell_y_tiled = self._tile_along_axis_2(cell_y, self._max_lines)
        random_x = np.random.uniform(0, self._cell_size, size=array_shape_3d)
        random_y = np.random.uniform(0, self._cell_size, size=array_shape_3d)
        x1 = cell_x_tiled + random_x
        y1 = cell_y_tiled + random_y
        return x1, y1

    def _relative_ending_points(
        self,
        cell_to_anchor_dx: np.ndarray,
        cell_to_anchor_dy: np.ndarray,
        angle_offset: float,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Return ending points of lines.

        NOTE: The ending points are calculated relative to origin. In order to
        get absolute position of the ending points, add these to starting
        points.
        """
        array_shape_3d = (self._rows, self._cols, self._max_lines)
        cell_to_anchor_angle = np.arctan2(cell_to_anchor_dy, cell_to_anchor_dx)
        angle = cell_to_anchor_angle + angle_offset
        angle_to_center_tiled = self._tile_along_axis_2(angle, self._max_lines)
        random_length = np.random.uniform(5, self._cell_size / 2, size=array_shape_3d)
        x2 = random_length * np.cos(angle_to_center_tiled)
        y2 = random_length * np.sin(angle_to_center_tiled)
        return x2, y2

    def _generate(
        self, anchor_point: Tuple[int, int], angle_offset: float
    ):  # pylint: disable=too-many-locals
        """Generate the line segments to be drawn.

        The Canvas is assumed a grid.
        Per grid cell a collection of random line segments are drawn.
        Number of line segments per grid cell is inversely proportional to distance to mouse.
        Angle of lines are the same per cell, and computed so that lines are aligned towards mouse.
        """

        col_indices, row_indices = np.meshgrid(
            np.arange(self._cols), np.arange(self._rows)
        )
        x1, y1 = self._starting_points(col_indices, row_indices)

        anchor_col, anchor_row = self._anchor_point_xy_to_rc(anchor_point)
        cell_to_anchor_dx = anchor_col - col_indices
        cell_to_anchor_dy = anchor_row - row_indices

        relative_x2, relative_y2 = self._relative_ending_points(
            cell_to_anchor_dx, cell_to_anchor_dy, angle_offset
        )
        x2 = relative_x2 + x1
        y2 = relative_y2 + y1

        distance = np.sqrt(cell_to_anchor_dx**2 + cell_to_anchor_dy**2)
        num_lines = np.clip(distance.astype(int), None, self._max_lines)

        lines = []
        for row in range(self._rows):
            for col in range(self._cols):
                n_lines = num_lines[row, col]
                x1_valid = x1[row, col, :n_lines]
                y1_valid = y1[row, col, :n_lines]
                x2_valid = x2[row, col, :n_lines]
                y2_valid = y2[row, col, :n_lines]

                for line_index in range(n_lines):
                    p1 = (x1_valid[line_index], y1_valid[line_index])
                    p2 = (x2_valid[line_index], y2_valid[line_index])
                    lines.append([p1, p2])
        return lines

    def draw(
        self,
        surface: pygame.surface.Surface,
        line_color: Color,
        anchor_point: Tuple[int, int],
        angle_offset: float,
    ):
        """Draw"""
        for line in self._generate(anchor_point, angle_offset):
            pygame.draw.line(surface, line_color, *line, 1)


class Controller:
    """Manages the application, including event handling, updating state, and rendering."""

    def __init__(
        self,
        draw_manager: DrawManager,
        surface: pygame.surface.Surface,
        gui_manager: pygame_gui.ui_manager.UIManager,
        gui_slider: pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider,
        background_color: Color,
        line_color: Color,
    ):
        self._draw_manager = draw_manager
        self._surface = surface
        self._gui_manager = gui_manager
        self._gui_slider = gui_slider
        self._background_color = background_color
        self._line_color = line_color
        self._running: bool = True
        self._mouse_pose: Tuple[int, int] = [0, 0]
        self._slider_value: float = 0.0

    @property
    def running(self) -> bool:
        """Return True if the process should keep running."""
        return self._running

    @staticmethod
    def _keep_running(event: pygame.event.Event) -> bool:
        """Return False if the game has quit, otherwise return True."""
        if event.type == pygame.locals.QUIT:
            return False
        if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
            return False
        return True

    def handle_events(self):
        """Handles user input and system events."""
        for event in pygame.event.get():
            self._running = self._keep_running(event)
            self._gui_manager.process_events(event)

    def update(self, time_delta: float):
        """Updates the Controller state."""
        self._mouse_pose = pygame.mouse.get_pos()
        self._slider_value = self._gui_slider.get_current_value()
        self._gui_manager.update(time_delta)

    def render(self):
        """Renders the game elements on the surface."""
        self._surface.fill(self._background_color)
        self._gui_manager.draw_ui(self._surface)
        self._draw_manager.draw(
            surface=self._surface,
            line_color=self._line_color,
            anchor_point=self._mouse_pose,
            angle_offset=self._slider_value,
        )
        pygame.display.flip()


@print_output()  # (print_func=print)
def _parse_arguments(argv: Sequence[str]):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--screen-width", type=int, default=1000)
    parser.add_argument("--screen-height", type=int, default=1000)
    parser.add_argument("--grid-size", type=int, default=30)
    parser.add_argument("--max-lines", type=int, default=60)
    args = parser.parse_args(argv)
    return args


def _init_pygame():
    try:
        pygame.init()
    except pygame.error as e:
        print(f"Failed to initialize Pygame: {e}")
        sys.exit(1)


def main(argv: Sequence[str]):
    """The main function initializes Pygame, sets up the game loop, and handles cleanup."""
    args = _parse_arguments(argv)

    slider_config = {
        "origin": (0, 0),
        "size": (args.screen_width, 20),
        "start_value": 0,
        "value_range": (0, np.pi / 2),
    }
    colors = {
        "background": WHITE,
        "line": BLACK,
    }

    _init_pygame()

    screen = pygame.display.set_mode((args.screen_width, args.screen_height))
    pygame.display.set_caption("Interactive Drawing Grid")
    clock = pygame.time.Clock()
    gui_manager = pygame_gui.UIManager((args.screen_width, args.screen_height))
    gui_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect(slider_config["origin"], slider_config["size"]),
        start_value=slider_config["start_value"],
        value_range=slider_config["value_range"],
        manager=gui_manager,
    )
    draw_manager = DrawManager(
        args.screen_width, args.screen_height, args.grid_size, args.max_lines
    )
    controller = Controller(
        draw_manager,
        screen,
        gui_manager,
        gui_slider,
        colors["background"],
        colors["line"],
    )

    while controller.running:
        time_delta = clock.tick(100) / 1000.0
        controller.handle_events()
        controller.update(time_delta)
        controller.render()

    pygame.quit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
