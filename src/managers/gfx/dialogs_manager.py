from src.controllers.window_controller import WindowController
from src.errors.dialog_error import DialogError
from src.globals import TYPE_CHECKING, curses
from src.interfaces.dialog_interface import DialogInterface

from ...assets.dialogs.menu.menu_dialog import MenuDialog

if TYPE_CHECKING:
    from src.controllers.selection_controller import SelectionController

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

        if not name or self.get(name):
            raise DialogError("Name not found")

        interface.default = False
        interface.game = self.game

        current_win = self.windows.window.win

        lines = getattr(interface, "lines", curses.LINES)
        columns = getattr(interface, "columns", curses.COLS)
        begin_x = getattr(interface, "x", 0)
        begin_y = getattr(interface, "y", 0)

        window = current_win.subwin(lines, columns, begin_x, begin_y)
        interface.win = window

        dialog = WindowController(self.game, interface)
        self.hidden_dialogs[name] = dialog

        dialog.win.erase()

        dialog.load_layer()
        dialog.load_keyboard()

        return interface

    def open(self, name: str, focus: bool = False) -> WindowController:
        dialog = self.hidden_dialogs.get(name)

        if not dialog:
            raise DialogError("Interface not found")

        self.dialogs[name] = dialog
        del self.hidden_dialogs[name]

        if focus:
            self.focus(name)

        return dialog

    def focus(self, name: str) -> bool:
        dialog = self.dialogs.get(name)

        if not dialog:
            return False

        self.focused = name

        has_selection, selection = self.has_selection(dialog)
        if has_selection:
            self.game.selection = selection

        return True

    def hide(self, name: str) -> bool:
        dialog = self.dialogs.get(name)

        if not dialog or not self.get(name):
            return False

        if self.focused == name:
            if self.has_selection(dialog):
                self.game.selection = None

            self.focused = None

        self.hidden_dialogs[name] = dialog
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

    def has_selection(
        self, dialog: WindowController
    ) -> tuple[bool, "SelectionController | None"]:
        has_selection = False
        selection = None

        if dialog.layer:
            for layer in dialog.layer.layers.values():
                has_selection = layer.has_selection
                if has_selection:
                    selection = layer.selection
                    break

        return has_selection, selection
