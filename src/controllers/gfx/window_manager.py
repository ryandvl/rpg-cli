import curses
from typing import TYPE_CHECKING

from src.controllers.gfx.layer_manager import LayerManager
from src.interfaces.window_interface import WindowInterface

from src.errors.window_error import WindowError

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from ..keyboard_manager import KeyboardManager


class WindowManager:
    """
    Manage all windows of the game and its layers
    """

    game_manager: "GameManager"
    keyboard_manager: "KeyboardManager"

    window: curses.window
    windows: dict[str, WindowInterface] = dict()

    current_window: str
    window_interface: WindowInterface
    last_window: str

    layer: "LayerManager" = None

    def setup(self, game_manager: "GameManager") -> None:
        """
        Initialize all necessary modules to run WindowManager
        """

        self.game_manager = game_manager
        self.keyboard_manager = game_manager.keyboard_manager

    def get_window(self, name: str) -> WindowInterface | None:
        """
        Get a stored window
        """

        return self.windows.get(name)

    def create_window(
        self,
        window_interface: WindowInterface,
    ) -> curses.window:
        """
        Create and register a new window
        """

        name = window_interface.name

        if not name:
            raise WindowError("Name not found")

        lines = getattr(window_interface, "lines", curses.LINES)
        columns = getattr(window_interface, "columns", curses.COLS)
        begin_x = getattr(window_interface, "x", 0)
        begin_y = getattr(window_interface, "y", 0)

        window = curses.newwin(lines, columns, begin_x, begin_y)

        self.register_window(name, window)

        return window

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
            self.current_window = name
            self.window_interface = window_interface
            self.last_window = name

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
        self.window_interface = window_interface

        self.window.clear()

        self.load_layers()
        self.load_keyboard()

        window_interface.window.refresh()

    def load_layers(self) -> None:
        """
        Load all layers from the current window
        """

        if self.layer:
            del self.layer

        self.layer = LayerManager(self.game_manager)

    def load_keyboard(self) -> None:
        """
        Load all keyboard inputs from the current window
        """

        if not self.layer:
            raise WindowError("Initialize layer first to initialize keyboard")

        self.keyboard_manager.clear_window()

        self.keyboard_manager.window_inputs = self.window_interface.window_inputs
        self.keyboard_manager.layer_inputs.clear()

        for layer in self.layer.layers.values():
            self.keyboard_manager.layer_inputs[layer.name] = layer.inputs
