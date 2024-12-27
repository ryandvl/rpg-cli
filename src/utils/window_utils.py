import curses

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers.hud_controller import HudController

def top_left_title(window: curses.window, title: str):
    y, _ = window.getbegyx()

    window.move(y - 1, 1)
    window.addstr(title)

def top_center_title(window: curses.window, title: str):
    y, _ = window.getbegyx()
    _, width = window.getmaxyx()

    window.move(y - 1, (width - len(title)) // 2)
    window.addstr(title)

def top_right_title(window: curses.window, title: str):
    y, _ = window.getbegyx()
    _, width = window.getmaxyx()

    window.move(y - 1, (width - len(title)) - 1)
    window.addstr(title)

def attr_on(window: curses.window, attr: int):
    window.attron(attr)

def attr_off(window: curses.window, attr: int):
    window.attroff(attr)
