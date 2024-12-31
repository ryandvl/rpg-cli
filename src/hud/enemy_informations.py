import curses
from typing import Any, Dict
from src.controllers import bar_controller
from src.controllers.bar_controller import BarController
from src.dto.layer_dto import LayerDTO
from src.utils.window_utils import *

class EnemyInformations(LayerDTO):
    current_health: float = 1
    total_health: float = 100
    bars: Dict[str, BarController] = dict()

    def render(self) -> None:
        window = curses.newwin(12, 30, 4, 40)

        set_border(window, self.gcp(0, 0))

        top_center_title(window, 'ENEMY', self.gcp(10, 0) | curses.A_BOLD)

        self.create_bar(
            window,
            name='HP',
            y=0,
            symbol='❤',
            symbol_color=self.gcp(125, 0) | curses.A_BOLD,
            name_color=self.gcp(0, 0) | curses.A_BOLD,
            get_func=self.health_bar,
            bar_color=self.gcp(0, 10) | curses.A_BOLD,
            bar_color_bg=self.gcp(0, 125) | curses.A_BOLD
        )

        window.refresh()

    def set_attr(self, key: str, value: Any):
        self.__setattr__(key, value)
        
        for bar_controller in self.bars.values():
            bar_controller.update()

    def health_bar(self):
        return (self.current_health, self.total_health)
        
    def create_bar(
            self,
            window: curses.window,
            y: int,
            symbol: str,
            name: str,
            symbol_color: int,
            name_color: int,
            bar_color: int,
            bar_color_bg: int,
            get_func: bar_controller.GET_FUNC
    ) -> BarController:
        write(window, symbol, 2, 2 + y, symbol_color)
        write(window, name, 4, 2 + y, name_color)

        bar = BarController(window, self.gcp, 7, 2 + y, 21, get_func)
        bar.set_bar_color(bar_color)
        bar.set_bar_color_bg(bar_color_bg)
        
        self.bars[name] = bar
        bar.update()
        
        return bar
