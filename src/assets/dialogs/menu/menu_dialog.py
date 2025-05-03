from src.interfaces.dialog_interface import DialogInterface

from .layers.menu_layer import MenuLayer


class MenuDialog(DialogInterface):
    name = "menu"
    priority = 1
    layers = list([MenuLayer()])

    def on_esc(self) -> None:
        pass
