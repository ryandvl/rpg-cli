import curses

from abc import ABC

from src.interfaces.layer_interface import LayerInterface


class WindowInterface(ABC):
    name: str
    window: curses.window
    layers: list[LayerInterface]
