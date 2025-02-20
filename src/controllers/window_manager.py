import curses

from typing import TYPE_CHECKING

from src.interfaces.window import WindowInterface

if TYPE_CHECKING:
    from .game_manager import GameManager

class WindowManager:
    game_manager: 'GameManager'

    window: curses.window
    windows: dict[str, WindowInterface] = dict()
    current_window: str = 'default'

    def __init__(self):
        pass

    def register_window(self, name: str, window: curses.window):
        window_interface = WindowInterface()
        window_interface.name = name
        window_interface.window = window

        self.windows[name] = window_interface

    def unregister_window(self, name: str):
        del self.windows[name]

    def change_window(self, window_interface: WindowInterface) -> None:
        self.current_window = window_interface.name

        self.window.clear()
        window_interface.window.refresh()    
