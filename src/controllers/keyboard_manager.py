import curses

from types import NoneType
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .game_manager import GameManager

type Func = Callable[[curses.window, KeyboardManager, int | None], NoneType]

class KeyboardManager:
    game_manager: 'GameManager'

    window: curses.window
    inputs: dict[str, Func] = dict()

    def __init__(self, game_manager: 'GameManager'):
        self.game_manager = game_manager

        curses.set_escdelay(25) # Default: 1000ms

    def set_window(self, window: curses.window) -> None:
        self.window = window

    def update(self) -> None:
        try:
            key = self.window.getch()
        except:
            key = None

        if key == 27: # ESC
            self.window.nodelay(True)

            key_combo = self.window.getch()
            if key_combo == -1:
                self.game_manager.is_running = False
                
            self.window.nodelay(False)

        for func in self.inputs.values():
            func(self.window, self, key)
