from src.globals import ABC, abstractmethod

from .window_interface import WindowInterface


class DialogInterface(WindowInterface, ABC):
    priority: int

    @abstractmethod
    def on_esc(self) -> None:
        pass
