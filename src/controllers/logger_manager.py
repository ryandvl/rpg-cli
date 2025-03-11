import curses
import re
from typing import TYPE_CHECKING

from src.config.colors_config import DARK_GRAY, LOGGER_BACKGROUND
from src.interfaces.logger_message_interface import LoggerMessageInterface
from src.interfaces.logger_message_part_interface import LoggerMessagePartInterface

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .window.window_manager import WindowManager
    from .hud_manager import HudManager


class LoggerManager:
    """
    Manage information messages on console
    """

    game_manager: "GameManager"
    window_manager: "WindowManager"
    hud_manager: "HudManager"

    logs: list[LoggerMessageInterface] = list()
    background: int = 0

    def setup(self, game_manager: "GameManager") -> None:
        """
        Initialize all necessary modules to run logger
        """

        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager
        self.hud_manager = game_manager.hud_manager

    def create_window(self) -> None:
        """
        Create the logger console window inside the default wrapper
        """

        self.background = self.hud_manager.get_color_pair(
            LOGGER_BACKGROUND[0], LOGGER_BACKGROUND[1]
        )

        self.window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        self.window_manager.register_window("logs", self.window)
        self.window.bkgd(self.background)

    def open_or_close_console(self) -> None:
        """
        Open or close the logger console
        """

        current_window = self.window_manager.current_window
        last_window = self.window_manager.last_window

        if current_window != "logs":
            self.info("$28,17$Opening logger...")

            self.window_manager.change_window("logs")

            self.success("Logger opened!")

            for log in self.logs:
                for message_part in log.message_parts:
                    self.window.addstr(message_part.message, message_part.color)

                self.window.addch("\n")
        else:
            self.window_manager.change_window(last_window)

    def clear(self) -> None:
        """
        Clear the logger console
        """

        self.logs.clear()

    def format_message(self, message: str) -> LoggerMessageInterface:
        """
        Format a message to include colors
        Example: "$10,1$Message with color"
        """

        expression: str = r"\$(\d+),(\d+)\$([^$]+)"

        logger_message = LoggerMessageInterface()
        logger_message.message_parts = list()

        def create_part(text: str, color_pair: int) -> None:
            logger_message_part = LoggerMessagePartInterface()
            logger_message_part.message = text
            logger_message_part.color = color_pair

            logger_message.message_parts.append(logger_message_part)

        for match in re.finditer(expression, message):
            foreground: int = int(match.group(1))
            background: int = int(match.group(2))
            text: str = match.group(3)

            color_pair: int = self.hud_manager.get_color_pair(foreground, background)

            create_part(text, color_pair)

        if len(logger_message.message_parts) == 0:
            create_part(message, self.background)

        return logger_message

    def print(self, message: str) -> None:
        """
        Print a message to logger console
        """

        formatted_message = self.format_message(message)
        self.logs.append(formatted_message)

    def info(self, message: str) -> None:
        """
        Print a information message to logger console
        """

        message = f"{DARK_GRAY}[$15,17$INFO{DARK_GRAY}] $16,17${message}"

        formatted_message = self.format_message(message)
        self.logs.append(formatted_message)

    def warn(self, message: str) -> None:
        """
        Print a warning message to logger console
        """

        message = f"{DARK_GRAY}[$12,17$WARNING{DARK_GRAY}] $227,17${message}"

        self.print(message)

    def success(self, message: str) -> None:
        """
        Print a success message to logger console
        """

        message = f"{DARK_GRAY}[$15,17$INFO{DARK_GRAY}] $47,17${message}"

        self.print(message)

    def error(self, message: str) -> None:
        """
        Print a error message to logger console
        """

        message = f"{DARK_GRAY}[$10,17$ERROR{DARK_GRAY}] $197,17${message}"

        self.print(message)
