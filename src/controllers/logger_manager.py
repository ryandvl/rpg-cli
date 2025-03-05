import curses

import re
from typing import TYPE_CHECKING

from src.interfaces.logger_message import LoggerMessageInterface
from src.interfaces.logger_message_part import LoggerMessagePartInterface

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .window_manager import WindowManager
    from .hud_manager import HudManager

class LoggerManager:
    game_manager: 'GameManager'
    window_manager: 'WindowManager'
    hud_manager: 'HudManager'

    window: curses.window
    logs: list[LoggerMessageInterface | str] = list()

    def setup(self, game_manager: 'GameManager') -> None:
        '''
        Initialize all necessary modules to run logger
        '''
        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager
        self.hud_manager = game_manager.hud_manager

    def create_window(self) -> None:
        '''
        Create the logger console window inside the default wrapper
        '''
        self.window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.window_manager.register_window('logs', self.window)
        self.window.bkgd(self.hud_manager.get_color_pair(16, 17))

    def open_or_close_console(self) -> None:
        '''
        Open or close the logger console
        '''
        current_window = self.window_manager.current_window
        last_window = self.window_manager.last_window

        if current_window != 'logs':
            self.info('$28,17$Opening logger...')

            self.window_manager.change_window('logs')

            self.success('Logger opened!')

            for log in self.logs:
                if isinstance(log, str):
                    self.window.addstr(log)
                else:
                    for message_part in log.message_parts:
                        self.window.addstr(
                            message_part.message,
                            message_part.color
                        )

                self.window.addch('\n')
        else:
            self.window_manager.change_window(last_window)

    def clear(self) -> None:
        '''
        Clear the logger console
        '''
        self.logs.clear()

    def format_message(self, message: str) -> LoggerMessageInterface | str:
        '''
        Format a message to include colors
        Example: "$10,1$Message with color"
        '''
        expression: str = r"\$(\d+),(\d+)\$([^$]+)"

        logger_message = LoggerMessageInterface()
        logger_message.message_parts = list()

        for match in re.finditer(expression, message):
            foreground: int = int(match.group(1))
            background: int = int(match.group(2))
            text: str = match.group(3)

            color_pair: int = self.hud_manager.get_color_pair(foreground, background)

            logger_message_part = LoggerMessagePartInterface()
            logger_message_part.message = text
            logger_message_part.color = color_pair

            logger_message.message_parts.append(logger_message_part)

        if len(logger_message.message_parts) == 0:
            return message

        return logger_message

    def print(self, message: str, format_message: bool = True) -> None:
        '''
        Print a message to logger console
        '''
        if format_message:
            formatted_message = self.format_message(message)
            self.logs.append(formatted_message)
            return

        self.logs.append(message)

    def info(self, message: str, format_message: bool = True) -> None:
        '''
        Print a information message to logger console
        '''
        message = f'$9,17$[$15,17$INFO$9,17$] $16,17${message}'

        if format_message:
            formatted_message = self.format_message(message)
            self.logs.append(formatted_message)
            return

        self.logs.append(message)

    def warn(self, message: str) -> None:
        '''
        Print a warning message to logger console
        '''
        message = f'$9,17$[$12,17$WARNING$9,17$] $227,17${message}'

        self.print(message)

    def success(self, message: str) -> None:
        '''
        Print a success message to logger console
        '''
        message = f'$9,17$[$15,17$INFO$9,17$] $47,17${message}'

        self.print(message)

    def error(self, message: str) -> None:
        '''
        Print a error message to logger console
        '''
        message = f'$9,17$[$10,17$ERROR$9,17$] $197,17${message}'

        self.print(message)
