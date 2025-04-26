from config import CONSOLE_WINDOW_NAME
from src.interfaces.window_interface import WindowInterface

from .layers.logs_layer import LogsLayer


class ConsoleWindow(WindowInterface):
    name = CONSOLE_WINDOW_NAME
    layers = list([LogsLayer()])
