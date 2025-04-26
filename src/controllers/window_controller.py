from src.globals import TYPE_CHECKING, curses

from ..controllers.layer_controller import LayerController
from ..errors.window_error import WindowError
from ..interfaces.window_interface import WindowInterface

if TYPE_CHECKING:
    from ..managers.game_manager import GameManager
    from ..managers.keyboard_manager import KeyboardManager


class WindowController:
    game: "GameManager"
    keyboard: "KeyboardManager"

    name: str
    win: curses.window
    interface: WindowInterface

    layer: LayerController | None = None

    def __init__(self, game: "GameManager", interface: WindowInterface) -> None:
        self.game = game
        self.keyboard = game.keyboard

        self.interface = interface
        self.name = interface.name
        self.win = interface.win

    def render(self) -> None:
        if layer := self.layer:
            layer.render()

    def load_layer(self) -> None:
        if self.layer:
            del self.layer

        self.layer = LayerController(self.game, self)
        self.layer.load(self.interface)

    def load_keyboard(self) -> None:
        if not self.layer:
            raise WindowError("Initialize layer first to initialize keyboard")

        self.keyboard.clear_window()
        self.keyboard.window_inputs = self.interface.inputs
        self.keyboard.layer_inputs.clear()

        for layer in self.layer.layers.values():
            self.keyboard.layer_inputs[layer.name] = layer.inputs
