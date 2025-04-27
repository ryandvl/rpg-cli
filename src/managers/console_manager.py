from datetime import datetime

from config import CONSOLE_BACKGROUND, CONSOLE_WINDOW_NAME, DARK_GRAY
from src.globals import TYPE_CHECKING, curses, re
from src.interfaces.log_message_interface import (
    LogMessageInterface,
    LogMessagePartInterface,
)

from ..assets.imports import ConsoleWindow

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .gfx.render_manager import RenderManager
    from .gfx.windows_manager import WindowsManager


class ConsoleManager:
    game: "GameManager"
    windows: "WindowsManager"
    render: "RenderManager"

    window: curses.window
    window_name: str = CONSOLE_WINDOW_NAME
    is_open: bool = False

    logs: list[LogMessageInterface] = list()
    background: int = 0

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.windows = game.windows
        self.render = game.render

    def load(self) -> None:
        self.background = self.render.get_color_pair(
            CONSOLE_BACKGROUND[0], CONSOLE_BACKGROUND[1]
        )

        self.window = self.windows.create(ConsoleWindow())

    def open(self) -> bool:
        if self.is_open:
            return False

        self.info("$28,17$Opening console...")

        self.windows.change(CONSOLE_WINDOW_NAME)

        self.success("Console opened!")

        self.is_open = True

        return True

    def close(self) -> bool:
        if not self.is_open:
            return False

        last_window = self.windows.last_window
        self.windows.change(last_window)

        self.is_open = False

        return True

    def open_or_close(self) -> None:
        self.close() if self.is_open else self.open()

    def clear(self) -> None:
        self.logs.clear()

    def format_message(self, message: str) -> LogMessageInterface:
        expression: str = r"\$(\d+),(\d+)\$([^$]+)"

        log_message = LogMessageInterface()
        log_message.message_parts = list()

        def create_part(text: str, color_pair: int) -> None:
            message_part = LogMessagePartInterface()
            message_part.message = text
            message_part.color = color_pair

            log_message.message_parts.append(message_part)

        for match in re.finditer(expression, message):
            foreground: int = int(match.group(1))
            background: int = int(match.group(2))
            text: str = match.group(3)

            color_pair: int = self.render.get_color_pair(foreground, background)

            create_part(text, color_pair)

        if len(log_message.message_parts) == 0:
            create_part(message, self.background)

        return log_message

    @staticmethod
    def format_time() -> str:
        time = datetime.now().strftime("%H:%M:%S")
        time_message = f"{DARK_GRAY}{time} "

        return time_message

    def print(self, message: str) -> None:
        formatted_message = self.format_message(self.format_time() + message)
        self.logs.append(formatted_message)

    def info(self, message: str) -> None:
        message = f"{DARK_GRAY}[$15,17$INFO{DARK_GRAY}] $16,17${message}"

        formatted_message = self.format_message(self.format_time() + message)
        self.logs.append(formatted_message)

    def warn(self, message: str) -> None:
        message = f"{DARK_GRAY}[$12,17$WARNING{DARK_GRAY}] $227,17${message}"

        self.print(message)

    def success(self, message: str) -> None:
        message = f"{DARK_GRAY}[$15,17$INFO{DARK_GRAY}] $47,17${message}"

        self.print(message)

    def error(self, message: str) -> None:
        message = f"{DARK_GRAY}[$10,17$ERROR{DARK_GRAY}] $197,17${message}"

        self.print(message)
