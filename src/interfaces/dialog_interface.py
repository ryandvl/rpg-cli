from src.globals import ABC

from .window_interface import WindowInterface


class DialogInterface(WindowInterface, ABC):
    priority: int

    def on_esc(self) -> None:
        pass
