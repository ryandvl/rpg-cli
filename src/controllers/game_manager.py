from curses import wrapper

from .window_manager import WindowManager
from .hud_manager import HudManager
from .keyboard_manager import KeyboardManager
from .logger_manager import LoggerManager

class GameManager:
    is_running: bool = False
    frames: int = 0

    window_manager: 'WindowManager' = WindowManager()
    logger_manager: 'LoggerManager' = LoggerManager()
    hud_manager: 'HudManager' = HudManager()
    keyboard_manager: 'KeyboardManager' = KeyboardManager()

    def __init__(self) -> None:
        self.window_manager.setup(self)
        self.logger_manager.setup(self)
        self.hud_manager.setup(self)
        self.keyboard_manager.setup(self)

    def run(self) -> None:
        self.is_running = True

        wrapper(self.hud_manager.wrapper)
