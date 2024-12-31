import curses

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from src.controllers.hud_controller import HudController
    from src.controllers.game_controller import GameController

type GCP = Callable[[int, int], int]

class LayerDTO:
    window: curses.window
    game_controller: 'GameController'
    hud_controller: 'HudController'
    gcp: Callable[[int, int], int]

    def __init__(self) -> None:
        pass

    def render(self) -> None:
        pass
