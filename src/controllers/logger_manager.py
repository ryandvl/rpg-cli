import curses

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .window_manager import WindowManager

class LoggerManager:
    game_manager: 'GameManager'
    window_manager: 'WindowManager'

    window: curses.window
    logs: list = []

    def setup(self, game_manager: 'GameManager') -> None:
        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager

    def create_window(self) -> None:
        self.window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.window_manager.register_window('logs', self.window)

    def print(self) -> None:
        pass
