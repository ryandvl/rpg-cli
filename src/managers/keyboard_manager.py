from types import NoneType
from typing import Callable

from src.globals import TYPE_CHECKING, curses, get_named_key

type KeyboardFunction = Callable[[curses.window, KeyboardManager, int | None], NoneType]

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .gfx.windows_manager import WindowsManager


class KeyboardManager:
    game: "GameManager"
    windows: "WindowsManager"

    layer_inputs: dict[str, dict[str, KeyboardFunction]] = dict()
    window_inputs: dict[str, KeyboardFunction] = dict()
    global_inputs: dict[str, KeyboardFunction] = dict()

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.windows = game.windows

        curses.set_escdelay(25)  # Default: 1000ms

    def update(self) -> None:
        window = self.windows.window.win

        try:
            key = window.getch()
        except:  # noqa: E722
            key = None

        # TODO: This is just for tests, remove later
        if key == get_named_key("esc"):
            if self.check_esc(window):
                self.game.stop()
                return

        for func in self.get_inputs().values():
            func(window, self, key)

    def get_input(self, input_name: str) -> KeyboardFunction | None:
        return self.global_inputs.get(input_name) or self.window_inputs.get(input_name)

    def get_inputs(self) -> dict:
        return self.layer_inputs | self.window_inputs | self.global_inputs

    def check_esc(self, window: curses.window) -> bool:
        window.nodelay(True)

        key_combo = window.getch()
        if key_combo == -1:
            return True

        window.nodelay(False)

        return False

    def clear_window(self) -> None:
        self.window_inputs.clear()
        self.layer_inputs.clear()
