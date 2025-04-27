from types import NoneType
from typing import Callable

from src.globals import TYPE_CHECKING, curses, get_named_key

type KeyboardFunction = Callable[[curses.window, KeyboardManager, int | None], NoneType]

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .gfx.dialogs_manager import DialogsManager
    from .gfx.windows_manager import WindowsManager


class KeyboardManager:
    game: "GameManager"
    windows: "WindowsManager"
    dialogs: "DialogsManager"

    layer_inputs: dict[str, dict[str, KeyboardFunction]] = dict()
    window_inputs: dict[str, KeyboardFunction] = dict()
    global_inputs: dict[str, KeyboardFunction] = dict()

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.windows = game.windows
        self.dialogs = game.dialogs

        curses.set_escdelay(25)  # Default: 1000ms

    def update(self) -> None:
        screen = self.windows.screen
        window = self.windows.window.win

        try:
            key = screen.getch()
        except:  # noqa: E722
            key = None

        # TODO: TEMPORARY
        if key == get_named_key("single_quotes"):
            self.game.console.open_or_close()
            return

        if key == curses.KEY_F4:
            # For emergencies situations
            return self.game.stop()
        elif not self.dialogs.focused and key == get_named_key("esc"):
            if self.check_esc(window):
                self.dialogs.show("menu")
                return

        for func in self.get_inputs():
            func(screen, self, key)

    def get_input(self, input_name: str) -> KeyboardFunction | None:
        return self.global_inputs.get(input_name) or self.window_inputs.get(input_name)

    def get_inputs(self) -> list:
        result = []

        result.extend(self.window_inputs.values())
        result.extend(self.global_inputs.values())

        for value in self.layer_inputs.values():
            result.extend(value.values())

        return result

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
