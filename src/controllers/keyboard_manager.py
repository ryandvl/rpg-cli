import curses
from types import NoneType
from typing import TYPE_CHECKING, Callable

from src.functions.keyboard import get_named_key

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .window.window_manager import WindowManager
    from .logger_manager import LoggerManager

type Func = Callable[[curses.window, KeyboardManager, int | None], NoneType]


class KeyboardManager:
    game_manager: "GameManager"
    window_manager: "WindowManager"
    logger_manager: "LoggerManager"

    layer_inputs: dict[str, dict[str, "Func"]] = dict()
    window_inputs: dict[str, "Func"] = dict()
    global_inputs: dict[str, "Func"] = dict()

    def setup(self, game_manager: "GameManager") -> None:
        """
        Initialize all necessary modules to run KeyboardManager
        """

        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager
        self.logger_manager = game_manager.logger_manager

        curses.set_escdelay(25)  # Default: 1000ms

    def update(self) -> None:
        """
        This is the default behavior, running per tick to detect keys
        """

        window = self.window_manager.window

        try:
            key = window.getch()
        except:  # noqa (Ruff Warning)
            key = None

        if key == get_named_key("esc"):
            self.check_close_request(window)
        elif key == get_named_key("single_quotes"):
            self.logger_manager.open_or_close_console()

        for func in self.get_inputs().values():
            func(window, self, key)

    def get_input(self, input_name: str) -> Func | None:
        """
        Get a input from Global, Window or Layer
        """

        return self.global_inputs.get(input_name) or self.window_inputs.get(input_name)

    def get_inputs(self) -> dict:
        """
        Get all inputs from Global, Window and Layer
        """

        return self.layer_inputs | self.window_inputs | self.global_inputs

    def check_close_request(self, window: curses.window) -> None:
        """
        Check if the player wants to exit the game
        """

        window.nodelay(True)

        key_combo = window.getch()
        if key_combo == -1:
            # Game has closed
            self.game_manager.stop()

        window.nodelay(False)

    def clear_window(self) -> None:
        """
        Clear window and layers inputs
        """

        self.window_inputs.clear()
        self.layer_inputs.clear()
