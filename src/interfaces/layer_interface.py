import curses

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from src.controllers.game_manager import GameManager
    from src.controllers.hud_manager import HudManager

type GCP = Callable[[int, int], int]


class LayerInterface(ABC):
    game_manager: "GameManager"
    hud_manager: "HudManager"

    name: str
    priority: int
    window: curses.window
    gcp: GCP
    """
    Get Color Pairs
    """

    @abstractmethod
    def render(self) -> None:
        """
        Render the Layer on Window
        """
