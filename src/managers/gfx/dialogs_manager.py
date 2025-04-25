from src.controllers.window_controller import WindowController
from src.errors.dialog_error import DialogError
from src.globals import TYPE_CHECKING, create_win, curses
from src.interfaces.window_interface import WindowInterface

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from .windows_manager import WindowsManager


class DialogsManager:
    game: "GameManager"
    windows: "WindowsManager"

    focused: str | None = None
    dialogs: dict[str, WindowController] = dict()
    hidden_dialogs: dict[str, WindowController] = dict()

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.windows = game.windows

    def get(self, name: str) -> WindowController | None:
        return self.dialogs.get(name)

    def get_focused(self) -> WindowController | None:
        return self.dialogs.get(self.focused) if self.focused else None

    def create(self, interface: WindowInterface) -> curses.window:
        name = interface.name

        if not name:
            raise DialogError("Name not found")

        lines = getattr(interface, "lines", 5)
        columns = getattr(interface, "columns", 10)
        begin_x = getattr(interface, "x", 0)
        begin_y = getattr(interface, "y", 0)

        window = create_win(lines, columns, begin_x, begin_y)

        self.__register(name, window)

        return window

    def focus(self, name: str) -> bool:
        dialog = self.dialogs.get(name)

        if not dialog:
            return False

        self.focused = name

        return True

    def hide(self, name: str) -> bool:
        dialog = self.hidden_dialogs.get(name)

        if dialog or not self.get(name):
            return False

        self.hidden_dialogs[name] = self.dialogs[name]
        del self.dialogs[name]

        return True

    def show(self, name: str) -> bool:
        dialog = self.dialogs.get(name)

        if not dialog or not self.get(name):
            return False

        self.dialogs[name] = self.hidden_dialogs[name]
        del self.hidden_dialogs[name]

        return True

    def delete(self, name: str) -> bool:
        if not self.get(name):
            return False

        self.__unregister(name)

        return True

    def __register(
        self, name: str, window: curses.window, default: bool = False
    ) -> WindowController:
        window_interface = WindowInterface()
        window_interface.name = name
        window_interface.win = window
        window_interface.default = False

        dialog = WindowController(self.game, window_interface)
        self.dialogs[name] = dialog

        dialog.win.clear()

        dialog.load_layer()
        dialog.load_keyboard()

        return self.dialogs[name]

    def __unregister(self, name: str) -> None:
        del self.dialogs[name]
        del self.hidden_dialogs[name]
