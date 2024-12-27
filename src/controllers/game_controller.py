from curses import wrapper
from src.controllers.hud_controller import HudController
from src.controllers.keyboard_controller import KeyboardController

class GameController:
    is_running: bool = False
    delta_time: int = 0
    hud_controller: 'HudController'
    keyboard_controller: 'KeyboardController'

    def __init__(self) -> None:
        self.hud_controller = HudController(self)
        self.keyboard_controller = KeyboardController(self)

    def run(self) -> None:
        self.is_running = True
        wrapper(self.hud_controller.wrapper)
