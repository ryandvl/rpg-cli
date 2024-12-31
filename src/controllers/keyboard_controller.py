import curses
from types import NoneType
from typing import TYPE_CHECKING, Callable

from src.data.keyboard_inputs import create_keyboard_inputs

if TYPE_CHECKING:
    from src.controllers.game_controller import GameController

type Func = Callable[[curses.window, KeyboardController, int | None], NoneType]

class KeyboardController:
    game_controller: 'GameController'
    window: curses.window
    inputs: dict[str, Func] = dict()

    def __init__(self, game_controller: 'GameController') -> None:
        self.game_controller = game_controller
        create_keyboard_inputs(self)
        curses.set_escdelay(25) # default: 1000ms

    def set_window(self, window: curses.window) -> None:
        self.window = window

    def create_input(self, name: str, func: Func) -> None:
        self.inputs[name] = func

    def delete_input(self, name: str) -> None:
        del self.inputs[name]

    def update(self) -> None:
        try:
            key = self.window.getch()
        except:
            key = None

        if key == 27: # ESC
            self.window.nodelay(True)

            key_combo = self.window.getch()
            if key_combo == -1:
                self.game_controller.is_running = False
                
            self.window.nodelay(False)

        for func in self.inputs.values():
            func(self.window, self, key)
