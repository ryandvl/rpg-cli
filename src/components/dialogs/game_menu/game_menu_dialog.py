from src.interfaces.dialog_interface import DialogInterface

from .layers.menu_layer import GameMenu_MenuLayer


class GameMenuDialog(DialogInterface):
    name = "game_menu"
    layers = list([GameMenu_MenuLayer])
