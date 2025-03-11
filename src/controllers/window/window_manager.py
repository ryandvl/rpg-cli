import curses

from src.controllers.game_manager import GameManager

from typing import TYPE_CHECKING

from src.controllers.window.layer_manager import LayerManager

if TYPE_CHECKING:
    from src.interfaces.window_interface import WindowInterface


class WindowManager:
    """
    Manage all windows of the game and its layers
    """

    game_manager: "GameManager"

    window: curses.window
    windows: dict[str, WindowInterface]
    layer: "LayerManager"

    def setup(self, game_manager: "GameManager") -> None:
        """
        Initialize all necessary modules to run WindowManager
        """

        self.game_manager = game_manager

    def get_window(self, name: str) -> WindowInterface | None:
        """
        Get a stored window
        """

        return self.windows.get(name)

    def register_window(self, name: str, window: curses.window) -> WindowInterface:
        """
        Register and store a window
        """

        window_interface = WindowInterface()
        window_interface.name = name
        window_interface.window = window

        self.windows[name] = window_interface

        if name == "default":
            self.window = window

        return window_interface

    def unregister_window(self, name: str) -> None:
        """
        Unregister a window
        """

        del self.windows[name]

    def change_window(self, name: str) -> None:
        """
        Change current window, this will clear the screen
        """

        window_interface = self.get_window(name)

        if not window_interface:
            return

        self.last_window = self.current_window

        self.window = window_interface.window
        self.current_window = window_interface.name

        self.window.clear()

        self.load_layers()

        window_interface.window.refresh()

    def load_layers(self) -> None:
        """
        Load all layers from the current window
        """

        if self.layer:
            del self.layer

        layer_manager = LayerManager(self.game_manager)

        self.layer = layer_manager
