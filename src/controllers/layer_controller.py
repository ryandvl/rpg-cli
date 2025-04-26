from src.globals import TYPE_CHECKING

from ..interfaces.layer_interface import LayerInterface
from ..interfaces.window_interface import WindowInterface

if TYPE_CHECKING:
    from ..managers.game_manager import GameManager
    from .window_controller import WindowController


class LayerController:
    game: "GameManager"
    window: "WindowController"

    layers: dict[str, LayerInterface] = dict()
    hidden_layers: dict[str, LayerInterface] = dict()
    sorted_layers: list[tuple[str, LayerInterface]] = list()

    def __init__(self, game: "GameManager", window: "WindowController") -> None:
        self.game = game
        self.window = window

    def load(self, interface: WindowInterface) -> None:
        for layer in interface.layers:
            self.create(layer)

    def get(self, name: str) -> LayerInterface:
        return self.layers[name] or self.hidden_layers[name]

    def render(self) -> None:
        for _, layer in self.sorted_layers:
            layer.draw()

    def create(self, interface: LayerInterface) -> LayerInterface | None:
        name = interface.name

        if self.hidden_layers.get(name):
            return

        interface.window = self.window.win

        interface.game = self.game
        interface.render = self.game.render

        interface.gcp = interface.render.get_color_pair

        self.layers[name] = interface
        self.__sort()

        return interface

    def __sort(self) -> None:
        layers = self.layers.items()

        self.sorted_layers = sorted(
            layers, key=lambda item: item[1].priority, reverse=True
        )
