import curses
from src.dto.layer_dto import LayerDTO
from src.utils.window_utils import *

class ChoicesBar(LayerDTO):
    def render(self) -> None:
        window = curses.newwin(5, 60, 17, 10)
        y, x = window.getbegyx()

        attack = window.subwin(3, 10, y + 1, x + 2)
        attack.bkgd(self.gcp(0, 12))
        set_border(attack, self.gcp(0, 12), True)
        write(attack, 'ATTACK', 1, 1, self.gcp(10, 0) | curses.A_BOLD)

        window.refresh()
