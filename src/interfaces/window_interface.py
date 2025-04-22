from src.globals import ABC, TYPE_CHECKING, curses

from .layer_interface import LayerInterface

if TYPE_CHECKING:
    from ..managers.keyboard_manager import KeyboardFunction


class WindowInterface(ABC):
    name: str
    win: curses.window
    default: bool = False
    layers: list[LayerInterface] = list()
    lines: int
    columns: int
    x: int
    y: int
    inputs: dict[str, "KeyboardFunction"] = dict()
