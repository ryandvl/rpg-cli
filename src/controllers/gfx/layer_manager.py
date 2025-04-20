from src.interfaces.layer_interface import LayerInterface

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from .hud_manager import HudManager
    from .window_manager import WindowManager


class LayerManager:
    """
    Manage all layers of a Window
    Initialized on a Change Window Event
    """

    game_manager: "GameManager"
    hud_manager: "HudManager"
    window_manager: "WindowManager"

    layers: dict[str, LayerInterface] = dict()
    hide_layers: dict[str, LayerInterface] = dict()

    def __init__(self, game_manager: "GameManager") -> None:
        self.game_manager = game_manager
        self.hud_manager = game_manager.hud_manager
        self.window_manager = game_manager.window_manager

    def create_layer(self, layer: LayerInterface) -> LayerInterface | None:
        """
        Create and store a new layer
        """

        name = layer.name

        if self.hide_layers.get(name):
            return

        layer.window = self.window_manager.window

        layer.game_manager = self.game_manager
        layer.hud_manager = self.hud_manager

        layer.gcp = self.hud_manager.get_color_pair

        if not layer.inputs:
            layer.inputs = dict()

        self.layers[name] = layer

        return layer

    def unhide_layer(self, layer_name: str) -> bool:
        """
        Unhide a Window Layer
        """

        if self.layers.get(layer_name):
            return False

        if not self.hide_layers.get(layer_name):
            return False

        self.layers[layer_name] = self.hide_layers[layer_name]
        del self.hide_layers[layer_name]

        return True

    def hide_layer(self, layer_name: str) -> bool:
        """
        Hide a Window Layer
        """

        if self.hide_layers.get(layer_name):
            return False

        if not self.layers.get(layer_name):
            return False

        self.hide_layers[layer_name] = self.layers[layer_name]
        del self.layers[layer_name]

        return True

    def delete_layer(self, layer_name: str) -> None:
        """
        Delete a Window Layer
        """

        if self.layers.get(layer_name):
            del self.layers[layer_name]
        elif self.hide_layers.get(layer_name):
            del self.hide_layers[layer_name]

    def get_layer(self, layer_name: str) -> LayerInterface:
        """
        Returns a Window Layer
        """

        return self.layers[layer_name] or self.hide_layers[layer_name]
