import curses

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from src.controllers.hud_controller import HudController
    from src.controllers.game_controller import GameController

class LayerDTO:
    window: curses.window
    game_controller: 'GameController'
    hud_controller: 'HudController'
    gcp: Callable[[str], int]

    def __init__(self) -> None:
        pass

    def render(self) -> None:
        pass
