import curses
from src.dto.layer_dto import LayerDTO
from src.utils.window_utils import *

class EnemyInformations(LayerDTO):
    def render(self) -> None:
        window = curses.newwin(6, 18, 1, 60)

        window.bkgd(self.gcp("BLACK_CYAN") | curses.A_BOLD)

        attr_on(window, self.gcp("WHITE_BLACK") | curses.A_BOLD)
        window.border()
        attr_off(window, self.gcp("WHITE_BLACK") | curses.A_BOLD)

        attr_on(window, self.gcp("RED_BLACK") | curses.A_BOLD)
        top_left_title(window, 'ENEMY')
        attr_off(window, self.gcp("RED_BLACK") | curses.A_BOLD)

        window.refresh()
