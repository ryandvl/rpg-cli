from curses import wrapper

from .hud_manager import HudManager
from .keyboard_manager import KeyboardManager

class GameManager:
    is_running: bool = False
    frames: int = 0

    hud_manager: 'HudManager'
    keyboard_manager: 'KeyboardManager'

    def __init__(self) -> None:
        self.hud_manager = HudManager(self)
        self.keyboard_manager = KeyboardManager(self)

        self.hud_manager.setup()

    def run(self) -> None:
        self.is_running = True

        wrapper(self.hud_manager.wrapper)
