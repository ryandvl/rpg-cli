from curses import wrapper

from .console_manager import ConsoleManager
from .gfx.render_manager import RenderManager
from .gfx.windows_manager import WindowsManager
from .keyboard_manager import KeyboardManager


class GameManager:
    console: "ConsoleManager"
    render: "RenderManager"
    keyboard: "KeyboardManager"
    windows: "WindowsManager"

    is_running: bool = False

    def __init__(self) -> None:
        self.console = ConsoleManager()
        self.render = RenderManager()
        self.windows = WindowsManager()
        self.keyboard = KeyboardManager()

        self.console.setup(self)
        self.render.setup(self)
        self.windows.setup(self)
        self.keyboard.setup(self)

    def run(self) -> None:
        self.is_running = True

        wrapper(self.render.wrapper)

    def stop(self) -> None:
        self.is_running = False
