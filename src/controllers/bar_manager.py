import curses

from typing import Callable, Tuple

from src.functions.string import *
from src.functions.window import *
from src.interfaces.layer import GCP

type GET_FUNC = Callable[[], Tuple[float, float]]

class BarManager:
    bar_size: int = 0
    bar_color: int = 0
    bar_color_bg: int = 0

    window: curses.window
    
    gcp: GCP
    get_func: GET_FUNC
    
    x: int
    y: int

    def __init__(self, window: curses.window, gcp: GCP, x: int, y: int, bar_size: int, get_func: GET_FUNC) -> None:
        self.window = window
        self.gcp = gcp
        self.x = x
        self.y = y
        self.bar_size = bar_size
        self.get_func = get_func

    def set_bar_color(self, value: int) -> None:
        self.bar_color = value

    def set_bar_color_bg(self, value: int) -> None:
        self.bar_color_bg = value

    def update(self) -> None:
        current, total = self.get_func()
        bar = create_bar(current, total, self.bar_size)

        write(self.window, bar[0], self.x, self.y, self.bar_color)
        write(self.window, bar[1], self.x + len(bar[0]), self.y, self.bar_color_bg)
