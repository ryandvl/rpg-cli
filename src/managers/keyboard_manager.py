from types import NoneType
from typing import Any, Callable

from src.assets.dialogs.menu.menu_dialog import MenuDialog
from src.globals import TYPE_CHECKING, curses, get_char_key, get_named_key

type KeyboardFunction = Callable[[curses.window, "GameManager", int | None], NoneType]

if TYPE_CHECKING:
    from .console_manager import ConsoleManager
    from .game_manager import GameManager
    from .gfx.dialogs_manager import DialogsManager
    from .gfx.render_manager import RenderManager
    from .gfx.windows_manager import WindowsManager


class KeyboardManager:
    game: "GameManager"
    windows: "WindowsManager"
    dialogs: "DialogsManager"
    render: "RenderManager"
    console: "ConsoleManager"

    layer_inputs: dict[str, dict[str, KeyboardFunction]] = dict()
    window_inputs: dict[str, KeyboardFunction] = dict()
    global_inputs: dict[str, KeyboardFunction] = dict()

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.windows = game.windows
        self.dialogs = game.dialogs
        self.render = game.render
        self.console = game.console

        curses.set_escdelay(25)  # Default: 1000ms

    def update(self, forced: bool = False) -> Any:
        screen = self.windows.screen

        try:
            key = screen.getch()
        except:  # noqa: E722
            key = None

        if key == get_named_key("f4"):
            # For emergencies situations
            return self.game.stop()

        if not self.render.is_valid_size:
            if key == get_char_key("q"):
                self.game.stop()

            return

        # TODO: TEMPORARY
        if key == get_named_key("single_quotes"):
            return self.console.open_or_close()
        elif not self.dialogs.focused and key == get_named_key("esc"):
            if self.check_esc(screen):
                if self.console.is_open:
                    return self.console.close()

                return self.dialogs.open(MenuDialog())

        for func in self.get_inputs():
            func(screen, self.game, key)

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
        key_combo = window.getch()
        if key_combo == -1:
            return True

        return False

    def clear_window(self) -> None:
        self.window_inputs.clear()
        self.layer_inputs.clear()
