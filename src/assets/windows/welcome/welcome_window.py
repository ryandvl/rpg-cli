from src.interfaces.layer_interface import LayerInterface
from src.interfaces.window_interface import WindowInterface


class WelcomeLayer(LayerInterface):
    name = "logs"
    priority = 1

    def draw(self) -> None:
        print("welcome")
        # self.window.addstr("welcome layer")


class WelcomeWindow(WindowInterface):
    name = "welcome"
    layers = list([WelcomeLayer()])
    default = True
