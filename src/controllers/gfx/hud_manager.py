import curses

from typing import TYPE_CHECKING

from src.functions.cursor import hide_cursor

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from ..logger_manager import LoggerManager
    from .window_manager import WindowManager


class HudManager:
    """
    Manage every hud parts of the game
    """

    game_manager: "GameManager"
    logger_manager: "LoggerManager"
    window_manager: "WindowManager"

    color_pairs: dict[str, int] = dict()

    def setup(self, game_manager: "GameManager") -> None:
        """
        Initialize all necessary modules to run HudManager
        """

        self.game_manager = game_manager
        self.logger_manager = game_manager.logger_manager
        self.window_manager = game_manager.window_manager

    def wrapper(self, window: curses.window) -> None:
        """
        Default curses wrapper to run the application, run per tick
        """

        curses.start_color()
        curses.use_default_colors()

        window_interface = self.window_manager.register_window("default", window)
        window_interface.window.bkgd(0, 1)

        hide_cursor()

        self.logger_manager.create_window()

        self.logger_manager.success("Game started!")
        self.render()

        while self.game_manager.is_running:
            self.render()

            self.game_manager.keyboard_manager.update()

    def create_color_pair(self, foreground: int, background: int) -> int:
        """
        Create and store a new color pair
        """

        newID: int = len(self.color_pairs.keys()) + 1
        name = str(foreground) + " " + str(background)

        curses.init_pair(newID, foreground, background)
        self.color_pairs[name] = curses.color_pair(newID)

        return self.color_pairs[name]

    def get_color_pair(self, foreground: int = 0, background: int = 0) -> int:
        """
        Get a stored color pair
        """

        foreground = foreground - 1
        background = background - 1

        name = str(foreground) + " " + str(background)

        if not self.color_pairs.get(name):
            return self.create_color_pair(foreground, background)

        return self.color_pairs[name]

    def render(self) -> None:
        """
        Render the current window screen
        """

        # TODO render all layers

        self.window_manager.window.refresh()
