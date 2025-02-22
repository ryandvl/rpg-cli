import curses

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from src.controllers.game_manager import GameManager
    from src.controllers.hud_manager import HudManager

type GCP = Callable[[int, int], int]

class LayerInterface(ABC):
    name: str
    window: curses.window
    game_manager: 'GameManager'
    hud_manager: 'HudManager'
    gcp: GCP

    @abstractmethod
    def render(self) -> None: pass
