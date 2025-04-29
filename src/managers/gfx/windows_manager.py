from src.assets.imports import WelcomeWindow
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
    screen: curses.window

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.keyboard = game.keyboard

    def load_default(self, stdscr: curses.window) -> None:
        self.screen = stdscr

        self.create(WelcomeWindow())

    def get(self, name: str) -> WindowInterface | None:
        return self.windows.get(name)

    def render(self, should_clear: bool = False) -> None:
        if should_clear:
            self.window.win.erase()

        self.window.render()

    def create(self, interface: WindowInterface) -> curses.window:
        if not interface.name:
            raise WindowError("Name not found")

        lines = getattr(interface, "lines", curses.LINES)
        columns = getattr(interface, "columns", curses.COLS)
        begin_x = getattr(interface, "x", 0)
        begin_y = getattr(interface, "y", 0)

        window = create_win(lines, columns, begin_x, begin_y)

        self.__register(window, interface)

        return window

    def change(self, name: str) -> bool:
        window_interface = self.get(name)

        if not window_interface:
            return False

        self.last_window = self.window.name

        del self.window
        self.window = WindowController(self.game, window_interface)

        self.window.win.erase()

        self.window.load_layer()
        self.window.load_keyboard()

        self.window.win.refresh()

        return True

    def __register(
        self, window: curses.window, interface: WindowInterface
    ) -> WindowInterface:
        interface.win = window

        self.windows[interface.name] = interface

        if interface.default:
            self.window = WindowController(self.game, interface)
            self.last_window = interface.name

        return interface

    def __unregister(self, name: str) -> None:
        del self.windows[name]
