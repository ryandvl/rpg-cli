import curses
from types import NoneType
from typing import TYPE_CHECKING, Callable

from src.data import hud_layers
from src.data.color_pairs import create_color_pairs
from src.dto.layer_dto import LayerDTO
from src.utils.cursor_utils import hide_cursor

if TYPE_CHECKING:
    from src.controllers.keyboard_controller import KeyboardController
    from src.controllers.game_controller import GameController

type FuncLayer = Callable[[curses.window, HudController], NoneType]

class HudController:
    game_controller: 'GameController'
    keyboard_controller: 'KeyboardController'
    color_pairs: dict[str, int] = dict()
    layers: dict[str, LayerDTO] = dict()
    hide_layers: dict[str, LayerDTO] = dict()
    window: curses.window

    def __init__(self, game_controller: 'GameController') -> None:
        self.game_controller = game_controller

    def wrapper(self, window: curses.window) -> None:
        self.keyboard_controller = self.game_controller.keyboard_controller

        self.window = window
        self.keyboard_controller.set_window(window)

        hide_cursor()

        curses.start_color()
        curses.use_default_colors()

        create_color_pairs(self)
        self.load_border()

        hud_layers.create_hud_layers(self)

        self.render()

        while self.game_controller.is_running:
            self.render()
            self.game_controller.keyboard_controller.update()
            
            self.game_controller.delta_time += 1

    def create_color_pair(self, name: str, foreground: int, background: int) -> None:
        newID: int = len(self.color_pairs.keys()) + 1

        curses.init_pair(newID, foreground, background)
        self.color_pairs[name.upper()] = curses.color_pair(newID)

    def get_color_pair(self, name: str) -> int:
        return self.color_pairs[name.upper()]
    
    def create_layer(self, name: str, dto: LayerDTO) -> None:
        if self.hide_layers.get(name):
            self.layers[name] = self.hide_layers[name]
            del self.hide_layers[name]
            return

        dto.window = self.window
        dto.hud_controller = self
        dto.game_controller = self.game_controller
        dto.gcp = self.get_color_pair
        
        self.layers[name] = dto

    def hide_layer(self, name: str) -> None:
        self.hide_layers[name] = self.layers[name]
        del self.layers[name]

    def load_border(self) -> None:
        self.window.attron(self.get_color_pair("WHITE_BLACK"))
        self.window.border()
        self.window.attroff(self.get_color_pair("WHITE_BLACK"))

    def render(self) -> None:
        for _, layer in self.layers.items():
            layer.render()
    
        self.window.refresh()
