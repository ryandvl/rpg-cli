import curses

from types import NoneType
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .window_manager import WindowManager

type Func = Callable[[curses.window, KeyboardManager, int | None], NoneType]

class KeyboardManager:
    game_manager: 'GameManager'
    window_manager: 'WindowManager'

    inputs: dict[str, Func] = dict()

    def setup(self, game_manager: 'GameManager') -> None:
        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager

        curses.set_escdelay(25) # Default: 1000ms

    def update(self) -> None:
        window = self.window_manager.window

        try:
            key = window.getch()
        except:
            key = None

        if key == 27: # ESC
            window.nodelay(True)

            key_combo = window.getch()
            if key_combo == -1:
                self.game_manager.is_running = False
                
            window.nodelay(False)
        elif key == 112: # P
            current_window = self.window_manager.current_window
            last_window = self.window_manager.last_window

            if current_window != 'logs':
                self.window_manager.change_window('logs')
                self.window_manager.window.addstr('foi pra logs ')
                last_window = current_window
            else:
                self.window_manager.change_window(last_window)
                self.window_manager.window.addstr('saiu de logs ')

        for func in self.inputs.values():
            func(self.window, self, key)
