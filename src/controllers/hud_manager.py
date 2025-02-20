import curses

from typing import TYPE_CHECKING

from src.functions.cursor import hide_cursor

if TYPE_CHECKING:
    from .game_manager import GameManager
    from .keyboard_manager import KeyboardManager

class HudManager:
    game_manager: 'GameManager'
    keyboard_manager: 'KeyboardManager'

    window: curses.window

    def __init__(self, game_manager: 'GameManager') -> None:
        self.game_manager = game_manager

    def setup(self) -> None:
        self.keyboard_manager = self.game_manager.keyboard_manager

    def wrapper(self, window: curses.window) -> None:
        self.window = window
        self.keyboard_manager.set_window(window)

        hide_cursor()

        curses.start_color()
        curses.use_default_colors()

        window.bkgd(0, 1)

        self.render()

        while self.game_manager.is_running:
            self.render()

            self.game_manager.keyboard_manager.update()
            self.game_manager.frames += 1

    def render(self) -> None:
        self.window.refresh()
