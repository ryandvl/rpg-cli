from src.globals import TYPE_CHECKING

from ..interfaces.layer_interface import LayerInterface

if TYPE_CHECKING:
    from ..managers.game_manager import GameManager
    from .window_controller import WindowController


class LayerController:
    game: "GameManager"
    window: "WindowController"

    layers: dict[str, LayerInterface] = dict()
    hidden_layers: dict[str, LayerInterface] = dict()

    def __init__(self, game: "GameManager", window: "WindowController") -> None:
        self.game = game
        self.window = window

    def get(self, name: str) -> LayerInterface:
        return self.layers[name] or self.hidden_layers[name]

    def create(self, interface: LayerInterface) -> LayerInterface | None:
        name = interface.name

        if self.hidden_layers.get(name):
            return

        interface.window = self.window.win

        interface.game = self.game
        interface.render = self.game.render

        interface.gcp = interface.render.get_color_pair

        if not interface.inputs:
            interface.inputs = dict()

        self.layers[name] = interface

        return interface
