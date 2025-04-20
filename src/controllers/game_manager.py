from curses import wrapper

from src.controllers.keyboard_manager import KeyboardManager

from .gfx.hud_manager import HudManager
from .gfx.window_manager import WindowManager
from .logger_manager import LoggerManager


class GameManager:
    """
    Manage all game resources, setup on initialization, use "run" function to start
    """

    logger_manager: "LoggerManager"
    hud_manager: "HudManager"
    window_manager: "WindowManager"

    is_running: bool = False

    def __init__(self) -> None:
        self.logger_manager = LoggerManager()
        self.hud_manager = HudManager()
        self.keyboard_manager = KeyboardManager()
        self.window_manager = WindowManager()

        self.logger_manager.setup(self)
        self.hud_manager.setup(self)
        self.keyboard_manager.setup(self)
        self.window_manager.setup(self)

    def run(self) -> None:
        """
        Start and run the game, call stop function to stop it
        """

        self.is_running = True

        wrapper(self.hud_manager.wrapper)

    def stop(self) -> None:
        """
        Stop and save all necessary sources
        """

        self.is_running = False
