# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=no-member
# pylint: disable=import-error

from typing import Any, Dict, Sequence, Tuple, Literal, TypedDict
import sys
import pygame
import pygame_gui


class Point(TypedDict):
    x: int
    y: int


class Line(TypedDict):
    p1: Point
    p2: Point


class Circle(TypedDict):
    p: Point
    r: float


PrimitiveType = Literal["line", "point", "circle"]
Primitive = Dict[PrimitiveType, Dict[str, Any]]


class DataModel:
    """
    - Provides raw or processed data for visualization
    - Manages computational logic, such as loading, filtering, or transformations"""

    def __init__(self):
        self.point1 = [100, 100]
        self.point2 = [200, 200]
        self.color = (255, 0, 0)  # Default color is red

    def update_points(self, offset):
        self.point1[0] = 100 + offset
        self.point2[0] = 200 + offset


class Visualization:
    """
    - Computes primitives based on state and data
    - Translates raw data into drawable forms"""

    def compute_primitives(self, data_model):
        # Prepare the two points and color for rendering
        return {
            "points": [data_model.point1, data_model.point2],
            "color": data_model.color,
        }


class Renderer:
    """
    - Draws primitives onto the screen
    - Handles drawing performance optimizations"""

    def draw(self, surface, primitives):
        # Draw the points and a line connecting them
        pygame.draw.line(
            surface,
            primitives["color"],
            primitives["points"][0],
            primitives["points"][1],
            3,
        )
        # pygame.draw.circle(surface, primitives["color"], primitives["points"][0], 5)
        # pygame.draw.circle(surface, primitives["color"], primitives["points"][1], 5)


class Controller:
    """
    - Updates state (e.g., zoom level, parameters)
    - Requests updated visual elements from Visualization"""

    def handle_ui_events(self, event, ui_manager, data_model):
        # Check directly for pygame_gui event types
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == ui_manager.slider:
                data_model.update_points(
                    int(event.value)
                )  # Update points based on slider value

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == ui_manager.radio_red:
                data_model.color = (255, 0, 0)  # Red
            elif event.ui_element == ui_manager.radio_blue:
                data_model.color = (0, 0, 255)  # Blue


class UIManager:
    """
    - Handles user input
    - Passes settings and parameters to Controller"""

    def __init__(self, screen_size):
        self.manager = pygame_gui.UIManager(screen_size)

        # Create a slider
        self.slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300, 500), (200, 30)),
            start_value=0,
            value_range=(-50, 50),
            manager=self.manager,
        )

        # Create radio buttons for color selection
        self.radio_red = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 500), (80, 30)),
            text="Red",
            manager=self.manager,
        )
        self.radio_blue = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 500), (80, 30)),
            text="Blue",
            manager=self.manager,
        )

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, surface):
        self.manager.draw_ui(surface)


class VisualizerApp:
    """
    - Initializes all components
    - Runs the main loop"""

    def __init__(self, screen_size: Tuple[int, int]):
        pygame.init()
        self._screen = pygame.display.set_mode(screen_size)
        self._clock = pygame.time.Clock()
        self._data_model = DataModel()
        self._visualization = Visualization()
        self._renderer = Renderer()
        self._controller = Controller()
        self._ui_manager = UIManager(self._screen.get_size())

    def run(self):
        running = True
        while running:
            time_delta = self._clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self._ui_manager.process_events(event)
                self._controller.handle_ui_events(
                    event, self._ui_manager, self._data_model
                )

            # Compute primitives for visualization
            primitives = self._visualization.compute_primitives(self._data_model)

            # Render the screen
            self._screen.fill((30, 30, 30))  # Clear the screen
            self._renderer.draw(self._screen, primitives)

            # Update and draw the UI
            self._ui_manager.update(time_delta)
            self._ui_manager.draw(self._screen)

            pygame.display.flip()

        pygame.quit()


def main(argv: Sequence[str]):
    _ = argv
    screen_size = (1000, 1000)
    app = VisualizerApp(screen_size)
    app.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
