import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers.hud_controller import HudController

BLACK = curses.COLOR_BLACK
RED = curses.COLOR_RED
GREEN = curses.COLOR_GREEN
YELLOW = curses.COLOR_YELLOW
BLUE = curses.COLOR_BLUE
MAGENTA = curses.COLOR_MAGENTA
CYAN = curses.COLOR_CYAN
WHITE = curses.COLOR_WHITE

BOLD = curses.A_BOLD

def create_color_pairs(h: 'HudController'):
    c = h.create_color_pair

    c('WHITE_BLACK', foreground=WHITE, background=BLACK)
    c('WHITE_RED', foreground=WHITE, background=RED)
    c('WHITE_YELLOW', foreground=WHITE, background=YELLOW)
    c('BLACK_WHITE', foreground=BLACK, background=WHITE)
    c('BLACK_CYAN', foreground=BLACK, background=CYAN)
    c('RED_BLACK', foreground=RED, background=BLACK)
    c('RED_WHITE', foreground=RED, background=WHITE)
