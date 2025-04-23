from src.interfaces.window_interface import WindowInterface

from .layers.logs_layer import LogsLayer


class ConsoleWindow(WindowInterface):
    name = "console"
    layers = list([LogsLayer()])
