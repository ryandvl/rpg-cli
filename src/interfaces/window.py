import curses

from abc import ABC

class WindowInterface(ABC):
    id: int
    name: str
    window: curses.window
    content: str
    layers: list
