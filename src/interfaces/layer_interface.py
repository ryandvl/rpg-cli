from typing import Callable

from src.globals import ABC, TYPE_CHECKING, abstractmethod, curses

if TYPE_CHECKING:
    from ..managers.game_manager import GameManager
    from ..managers.gfx.render_manager import RenderManager
    from ..managers.keyboard_manager import KeyboardFunction

type GetColorPairs = Callable[[int, int], int]


class LayerInterface(ABC):
    game: "GameManager"
    render: "RenderManager"

    name: str
    priority: int
    window: curses.window
    gcp: "GetColorPairs"
    inputs: dict[str, "KeyboardFunction"] = dict()

    @abstractmethod
    def draw(self) -> None:
        pass
