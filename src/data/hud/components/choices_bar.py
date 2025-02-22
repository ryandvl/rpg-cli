import curses

from src.interfaces.layer import LayerInterface

from src.functions.window import *

class ChoicesBar(LayerInterface):
    name: str = 'ChoicesBar'

    def render(self) -> None:
        window = curses.newwin(5, 60, 17, 10)
        y, x = window.getbegyx()

        attack = window.subwin(3, 10, y + 1, x + 2)
        set_border(attack, self.gcp(0, 255), True)
        write(attack, 'ATTACK', 1, 1, self.gcp(10, 0) | curses.A_BOLD)

        window.refresh()
