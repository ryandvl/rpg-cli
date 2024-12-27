import curses
from src.dto.layer_dto import LayerDTO
from src.utils.string_manipulation import create_bar
from src.utils.window_utils import *

class EnemyInformations(LayerDTO):
    def render(self) -> None:
        window = curses.newwin(12, 30, 4, 40)

        window.bkgd(self.gcp("BLACK_WHITE"))

        set_border(window, self.gcp("WHITE_BLACK"))

        top_left_title(window, 'ENEMY', self.gcp("RED_BLACK") | curses.A_BOLD)

        write(window, '❤', 2, 2, self.gcp("RED_WHITE") | curses.A_BOLD)
        write(window, 'HP', 4, 2, self.gcp("BLACK_WHITE") | curses.A_BOLD)
        write(window, create_bar(10, 10, 21), 7, 2, self.gcp("WHITE_RED") | curses.A_BOLD)

        window.refresh()
