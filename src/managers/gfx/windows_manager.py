from src.globals import TYPE_CHECKING, create_win, curses

from ...controllers.window_controller import WindowController
from ...errors.window_error import WindowError
from ...interfaces.window_interface import WindowInterface

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from ..keyboard_manager import KeyboardManager


class WindowsManager:
    game: "GameManager"
    keyboard: "KeyboardManager"

    last_window: str
    window: "WindowController"
    windows: dict[str, "WindowInterface"] = dict()

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.keyboard = game.keyboard

    def load(self, window: curses.window) -> WindowInterface:
        return self.__register("default", window, True)

    def get(self, name: str) -> WindowInterface | None:
        return self.windows.get(name)

    def create(self, interface: WindowInterface) -> curses.window:
        name = interface.name

        if not name:
            raise WindowError("Name not found")

        lines = getattr(interface, "lines", curses.LINES)
        columns = getattr(interface, "columns", curses.COLS)
        begin_x = getattr(interface, "x", 0)
        begin_y = getattr(interface, "y", 0)

        window = create_win(lines, columns, begin_x, begin_y)

        self.__register(name, window)

        return window

    def change(self, name: str) -> bool:
        window_interface = self.get(name)

        if not window_interface:
            return False

        self.last_window = self.window.name
        self.window = WindowController(self.game, window_interface)

        self.window.win.clear()

        self.window.load_layers()
        self.window.load_keyboard()

        self.window.win.refresh()

        return True

    def __register(
        self, name: str, window: curses.window, default: bool = False
    ) -> WindowInterface:
        window_interface = WindowInterface()
        window_interface.name = name
        window_interface.win = window
        window_interface.default = default

        self.windows[name] = window_interface

        if window_interface.default:
            self.window = WindowController(self.game, window_interface)
            self.last_window = name

        return window_interface

    def __unregister(self, name: str) -> None:
        del self.windows[name]
