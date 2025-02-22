import curses

from types import NoneType
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .window_manager import WindowManager
    from .logger_manager import LoggerManager

type Func = Callable[[curses.window, KeyboardManager, int | None], NoneType]

class KeyboardManager:
    game_manager: 'GameManager'
    window_manager: 'WindowManager'
    logger_manager: 'LoggerManager'

    inputs: dict[str, Func] = dict()

    def setup(self, game_manager: 'GameManager') -> None:
        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager
        self.logger_manager = game_manager.logger_manager

        curses.set_escdelay(25) # Default: 1000ms

    def update(self) -> None:
        window = self.window_manager.window

        try:
            key = window.getch()
        except:
            key = None

        if key == 27: # Key: ESC
            window.nodelay(True)

            key_combo = window.getch()
            if key_combo == -1:
                self.game_manager.is_running = False
                
            window.nodelay(False)
        elif key == 112: # Key: P
            self.logger_manager.open_or_close_console()

        for func in self.inputs.values():
            func(self.window, self, key)
