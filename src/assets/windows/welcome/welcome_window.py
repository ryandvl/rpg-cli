from src.interfaces.layer_interface import LayerInterface
from src.interfaces.window_interface import WindowInterface


class WelcomeLayer(LayerInterface):
    name = "logs"
    priority = 1

    def draw(self) -> None:
        screen = self.util

        screen.erase()

        screen.add_string("welcome", x=0, y=0)


class WelcomeWindow(WindowInterface):
    name = "welcome"
    layers = list([WelcomeLayer()])
    default = True
