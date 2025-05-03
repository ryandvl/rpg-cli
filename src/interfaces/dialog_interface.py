from src.globals import ABC, TYPE_CHECKING, abstractmethod

from .window_interface import WindowInterface

if TYPE_CHECKING:
    from src.managers.game_manager import GameManager


class DialogInterface(WindowInterface, ABC):
    game: "GameManager"
    priority: int

    def close(self) -> None:
        self.game.dialogs.close(self.name)

    @abstractmethod
    def on_esc(self) -> None:
        pass
