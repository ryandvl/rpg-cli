from src.components.windows.logger.layers.logs_layer import LogsLayer
from src.interfaces.window_interface import WindowInterface


class LoggerWindow(WindowInterface):
    name = "logger"
    layers = list([LogsLayer()])
