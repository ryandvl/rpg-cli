from src.controllers.window_controller import WindowController
from src.errors.dialog_error import DialogError
from src.globals import TYPE_CHECKING, curses
from src.interfaces.dialog_interface import DialogInterface

from ...assets.dialogs.menu.menu_dialog import MenuDialog

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from .windows_manager import WindowsManager


class DialogsManager:
    game: "GameManager"
    windows: "WindowsManager"

    focused: str | None = None
    dialogs: dict[str, WindowController] = dict()
    hidden_dialogs: dict[str, WindowController] = dict()
    interfaces: dict[str, DialogInterface] = dict()

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.windows = game.windows

    def load(self) -> None:
        self.register(MenuDialog())

    def get(self, name: str) -> WindowController | None:
        return self.dialogs.get(name) or self.hidden_dialogs.get(name)

    def get_focused(self) -> WindowController | None:
        return self.dialogs.get(self.focused) if self.focused else None

    def render(self) -> None:
        for dialog in self.dialogs.values():
            dialog.render()

    def register(self, interface: DialogInterface) -> DialogInterface:
        name = interface.name

        if not name or self.interfaces.get(name):
            raise DialogError("Name not found")

        interface.default = False
        interface.game = self.game

        self.interfaces[name] = interface

        return interface

    def open(self, name: str, focus: bool = False) -> WindowController:
        interface = self.interfaces.get(name)

        if not interface:
            raise DialogError("Interface not found")

        current_win = self.windows.window.win

        lines = getattr(interface, "lines", curses.LINES)
        columns = getattr(interface, "columns", curses.COLS)
        begin_x = getattr(interface, "x", 0)
        begin_y = getattr(interface, "y", 0)

        window = current_win.subwin(lines, columns, begin_x, begin_y)
        interface.win = window

        dialog = WindowController(self.game, interface)
        self.dialogs[name] = dialog

        dialog.win.erase()

        dialog.load_layer()
        dialog.load_keyboard()

        if focus:
            self.focus(interface.name)

        return dialog

    def close(self, name: str) -> bool:
        dialog = self.dialogs.get(name)

        if not dialog:
            return False

        self.hide(name)

        return True

    def focus(self, name: str) -> bool:
        dialog = self.dialogs.get(name)

        if not dialog:
            return False

        self.focused = name

        return True

    def hide(self, name: str) -> bool:
        dialog = self.dialogs.get(name)

        if not dialog or not self.get(name):
            return False

        if self.focused == name:
            self.focused = None

        self.hidden_dialogs[name] = self.dialogs[name]
        del self.dialogs[name]

        return True

    def show(self, name: str) -> bool:
        dialog = self.hidden_dialogs.get(name)

        if not dialog or not self.get(name):
            return False

        self.dialogs[name] = self.hidden_dialogs[name]
        del self.hidden_dialogs[name]

        return True

    def delete(self, name: str) -> bool:
        if not self.get(name):
            return False

        del self.dialogs[name]
        del self.hidden_dialogs[name]

        return True
