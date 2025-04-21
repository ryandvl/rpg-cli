from typing import TYPE_CHECKING

from src.interfaces.dialog_interface import DialogInterface

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from .window_manager import WindowManager


class DialogManager:
    """
    Manage all dialogs of the window
    Initialized on a Change Window Event
    """

    game_manager: "GameManager"
    window_manager: "WindowManager"

    dialogs: dict[str, DialogInterface] = dict()
    hidden_dialogs: dict[str, DialogInterface] = dict()

    def __init__(self, game_manager: "GameManager") -> None:
        self.game_manager = game_manager
        self.window_manager = game_manager.window_manager

    def get_dialog(self, dialog_name: str) -> DialogInterface:
        """
        Returns a Dialog
        """

        return self.dialogs[dialog_name] or self.hidden_dialogs[dialog_name]

    def show_dialog(self, dialog_name: str) -> bool:
        """
        Unhide a Dialog
        """

        if self.dialogs.get(dialog_name):
            return False

        if not self.hidden_dialogs.get(dialog_name):
            return False

        self.dialogs[dialog_name] = self.hidden_dialogs[dialog_name]
        del self.hidden_dialogs[dialog_name]

        return True

    def hide_dialog(self, dialog_name: str) -> bool:
        """
        Hide a Dialog
        """

        if self.hidden_dialogs.get(dialog_name):
            return False

        if not self.dialogs.get(dialog_name):
            return False

        self.hidden_dialogs[dialog_name] = self.dialogs[dialog_name]
        del self.dialogs[dialog_name]

        return True

    def delete_dialog(self, dialog_name: str) -> None:
        """
        Delete a Dialog
        """

        if self.dialogs.get(dialog_name):
            del self.dialogs[dialog_name]
        elif self.hidden_dialogs.get(dialog_name):
            del self.hidden_dialogs[dialog_name]
