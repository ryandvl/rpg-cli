import curses

from typing import TYPE_CHECKING

from src.functions.cursor import hide_cursor
from src.interfaces.layer import LayerInterface

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .keyboard_manager import KeyboardManager
    from .window_manager import WindowManager
    from .logger_manager import LoggerManager

class HudManager:
    game_manager: 'GameManager'
    keyboard_manager: 'KeyboardManager'
    window_manager: 'WindowManager'
    logger_manager: 'LoggerManager'
    layers: dict[str, LayerInterface] = dict()

    def setup(self, game_manager: 'GameManager') -> None:
        self.game_manager = game_manager
        self.keyboard_manager = game_manager.keyboard_manager
        self.window_manager = game_manager.window_manager
        self.logger_manager = game_manager.logger_manager

    def wrapper(self, window: curses.window) -> None:
        window_interface = self.window_manager.register_window('default', window)
        window_interface.window.addstr("Default content")

        self.logger_manager.create_window()

        hide_cursor()

        curses.start_color()
        curses.use_default_colors()

        window_interface.window.bkgd(0, 1)

        self.render()

        while self.game_manager.is_running:
            self.render()

            self.game_manager.keyboard_manager.update()
            self.game_manager.frames += 1

    def create_layer(self, layer: LayerInterface) -> None:
        name = layer.name

        if self.hide_layers.get(name):
            self.layers[name] = self.hide_layers[name]
            del self.hide_layers[name]
            return

        layer.window = self.window
        layer.hud_controller = self
        layer.game_manager = self.game_manager
        # layer.gcp = self.get_color_pair
        
        self.layers[name] = layer

    def render(self) -> None:
        for layer in self.layers.values():
            layer.render()
        
        self.window_manager.window.refresh()
