"""Interactive visualization with pygame.

A distribution of line segments that are all aligned towards the mouse position.

Discrete Mode.
"""

# pylint: disable=no-name-in-module, no-member, c-extension-no-member

from typing import Sequence
import argparse
import sys
import math
import random
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
        """Draws the grid with line segments in each cell, influenced by the mouse position."""
        # Calculate the center cell based on the mouse position
        center_col = mouse_x // self.cell_size
        center_row = mouse_y // self.cell_size
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculate the position of the current cell
                cell_x = col * self.cell_size
                cell_y = row * self.cell_size
                # Calculate the angle from the current cell to the center cell
                dx = center_col - col
                dy = center_row - row
                angle_to_center = math.atan2(dy, dx)
                # Determine the number of lines based on the distance to the center cell
                distance = math.sqrt(dx**2 + dy**2)
                num_lines = min(int(distance * 2), self.max_lines)
                # Draw random line segments in the cell
                for _ in range(num_lines):
                    x1 = cell_x + random.uniform(0, self.cell_size)
                    y1 = cell_y + random.uniform(0, self.cell_size)
                    length = random.uniform(5, self.cell_size / 2)
                    x2 = x1 + length * math.cos(angle_to_center)
                    y2 = y1 + length * math.sin(angle_to_center)
                    pygame.draw.line(surface, color, (x1, y1), (x2, y2), 1)


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
    parser.add_argument("--max-lines", type=int, default=30)
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
        clock.tick(50)

    pygame.quit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
