import curses

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .window_manager import WindowManager

class LoggerManager:
    game_manager: 'GameManager'
    window_manager: 'WindowManager'

    window: curses.window
    logs: list[str] = list()

    def setup(self, game_manager: 'GameManager') -> None:
        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager

    def open_or_close_console(self) -> None:
        current_window = self.window_manager.current_window
        last_window = self.window_manager.last_window

        if current_window != 'logs':
            self.window_manager.change_window('logs')

            self.print('Logger oppened!')

            for log in self.logs:
                self.window.addstr(log + '\n')
        else:
            self.print('Logger closed!')
            self.window_manager.change_window(last_window)

    def create_window(self) -> None:
        self.window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.window_manager.register_window('logs', self.window)

    def clear(self) -> None:
        self.logs.clear()

    def print(self, message: str) -> None:
        self.logs.append(message)
