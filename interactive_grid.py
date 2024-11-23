"""Interactive visualization with pygame.

A distribution of line segments that are all aligned towards the mouse position.

Discrete Mode.
"""

# pylint: disable=no-name-in-module, no-member, c-extension-no-member

from typing import Sequence
import argparse
import sys
import numpy as np
import pygame
import pygame.locals

from libs.colors import parse_color, BLACK, WHITE, Color
from libs.utils import print_output


class Canvas:  # pylint: disable=too-few-public-methods
    """Represents the basis for drawing on the pygame.surface.Surface."""

    def __init__(self, width, height, cell_size, max_lines):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.max_lines = max_lines
        self.rows = self.height // self.cell_size
        self.cols = self.width // self.cell_size

    def draw(
        self, surface: pygame.surface.Surface, mouse_x: int, mouse_y: int, color: Color
    ):  # pylint: disable=too-many-locals
        """Draws the line segments influenced by the mouse position.

        The Canvas is assumed a grid.
        Per grid cell a collection of random line segments are drawn.
        Number of line segments per grid cell is inversely proportional to distance to mouse.
        Angle of lines are the same per cell, and computed so that lines are aligned towards mouse.
        """

        def _tile_along_axis_2(arr):
            return np.tile(arr[:, :, None], (1, 1, self.max_lines))

        center_col = mouse_x // self.cell_size
        center_row = mouse_y // self.cell_size

        shape_3d = (self.rows, self.cols, self.max_lines)

        col_indices, row_indices = np.meshgrid(
            np.arange(self.cols), np.arange(self.rows)
        )
        cell_x = col_indices * self.cell_size
        cell_y = row_indices * self.cell_size
        cell_x_tiled = _tile_along_axis_2(cell_x)
        cell_y_tiled = _tile_along_axis_2(cell_y)
        random_x = np.random.uniform(0, self.cell_size, size=shape_3d)
        random_y = np.random.uniform(0, self.cell_size, size=shape_3d)
        x1 = cell_x_tiled + random_x
        y1 = cell_y_tiled + random_y

        dx = center_col - col_indices
        dy = center_row - row_indices
        angle_to_center = np.arctan2(dy, dx) + np.pi / 4
        angle_to_center_tiled = _tile_along_axis_2(angle_to_center)
        random_length = np.random.uniform(5, self.cell_size / 2, size=shape_3d)
        x2 = x1 + random_length * np.cos(angle_to_center_tiled)
        y2 = y1 + random_length * np.sin(angle_to_center_tiled)

        distance = np.sqrt(dx**2 + dy**2)
        num_lines = np.clip(distance.astype(int), None, self.max_lines)

        for row in range(self.rows):
            for col in range(self.cols):
                n_lines = num_lines[row, col]
                x1_valid = x1[row, col, :n_lines]
                y1_valid = y1[row, col, :n_lines]
                x2_valid = x2[row, col, :n_lines]
                y2_valid = y2[row, col, :n_lines]

                for line_index in range(n_lines):
                    pygame.draw.line(
                        surface,
                        color,
                        (x1_valid[line_index], y1_valid[line_index]),
                        (x2_valid[line_index], y2_valid[line_index]),
                        1,
                    )


class Controller:
    """Manages the application, including event handling, updating state, and rendering."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.running = True

    def handle_events(self):
        """Handles user input and system events."""
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                self.running = False
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    self.running = False

    def update(self):
        """Updates the Controller state."""

    def render(
        self,
        surface: pygame.surface.Surface,
        background_color: Color,
        line_color: Color,
    ):
        """Renders the game elements on the surface."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        surface.fill(background_color)
        self.canvas.draw(surface, mouse_x, mouse_y, line_color)
        pygame.display.flip()


@print_output(print_func=print)
def _parse_arguments(argv: Sequence[str]):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--screen-width", type=int, default=1000)
    parser.add_argument("--screen-height", type=int, default=1000)
    parser.add_argument("--grid-size", type=int, default=30)
    parser.add_argument("--max-lines", type=int, default=60)
    parser.add_argument("--background-color", type=parse_color, default=WHITE)
    parser.add_argument("--line-color", type=parse_color, default=BLACK)
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
    _init_pygame()

    screen = pygame.display.set_mode((args.screen_width, args.screen_height))
    pygame.display.set_caption("Interactive Drawing Grid")
    clock = pygame.time.Clock()
    canvas = Canvas(
        args.screen_width, args.screen_height, args.grid_size, args.max_lines
    )
    controller = Controller(canvas)

    while controller.running:
        controller.handle_events()
        controller.update()
        controller.render(screen, args.background_color, args.line_color)
        clock.tick(100)

    pygame.quit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
