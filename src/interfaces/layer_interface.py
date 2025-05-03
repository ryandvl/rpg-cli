from typing import Callable

from src.globals import ABC, TYPE_CHECKING, abstractmethod, curses
from src.utils.window import WindowUtil

if TYPE_CHECKING:
    from ..controllers.selection_controller import SelectionController
    from ..managers.console_manager import ConsoleManager
    from ..managers.game_manager import GameManager
    from ..managers.gfx.render_manager import RenderManager
    from ..managers.keyboard_manager import KeyboardFunction

type GetColorPairs = Callable[[int, int], int]


class LayerInterface(ABC):
    game: "GameManager"
    render: "RenderManager"
    console: "ConsoleManager"

    name: str
    priority: int
    window: curses.window
    gcp: "GetColorPairs"
    inputs: dict[str, "KeyboardFunction"] = dict()
    selection: "SelectionController"
    has_selection: bool = False

    util: WindowUtil

    def load(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
