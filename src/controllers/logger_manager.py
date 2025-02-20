import curses

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_manager import GameManager

class LoggerManager:
    game_manager: 'GameManager'

    window: curses.window 
    logs: list = []

    def __init__(self, game_manager: 'GameManager'):
        self.game_manager = game_manager
        self.window = curses.newwin(curses.LINES, curses.COLS, 0, 0)
        
        

    def print(self):
        pass
