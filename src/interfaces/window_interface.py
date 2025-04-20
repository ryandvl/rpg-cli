import curses
from abc import ABC
from typing import TYPE_CHECKING

from src.interfaces.layer_interface import LayerInterface

if TYPE_CHECKING:
    from src.controllers.keyboard_manager import Func


class WindowInterface(ABC):
    name: str
    window: curses.window
    layers: list[LayerInterface] = list()
    lines: int
    columns: int
    x: int
    y: int
    window_inputs: dict[str, "Func"] = dict()
