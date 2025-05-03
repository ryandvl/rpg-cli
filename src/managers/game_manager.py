import sys
from curses import wrapper

from src.globals import TYPE_CHECKING

from .console_manager import ConsoleManager
from .gfx.dialogs_manager import DialogsManager
from .gfx.render_manager import RenderManager
from .gfx.windows_manager import WindowsManager
from .keyboard_manager import KeyboardManager

if TYPE_CHECKING:
    from src.controllers.selection_controller import SelectionController


class GameManager:
    console: "ConsoleManager"
    render: "RenderManager"
    windows: "WindowsManager"
    dialogs: "DialogsManager"
    keyboard: "KeyboardManager"

    selection: "SelectionController | None" = None

    is_running: bool = False
    loaded: bool = False

    def __init__(self) -> None:
        self.console = ConsoleManager()
        self.render = RenderManager()
        self.windows = WindowsManager()
        self.dialogs = DialogsManager()
        self.keyboard = KeyboardManager()

        self.console.setup(self)
        self.render.setup(self)
        self.windows.setup(self)
        self.dialogs.setup(self)
        self.keyboard.setup(self)

        self.loaded = True

    def run(self) -> None:
        self.is_running = True

        reason = None
        if len(sys.argv) > 1 and sys.argv[1] == "--debug":
            wrapper(self.render.wrapper)
        else:
            try:
                wrapper(self.render.wrapper)
            except Exception as e:
                reason = str(e)
            finally:
                if reason:
                    print(f"Game closed, reason:\n{reason}")
                else:
                    print("Game closed")

    def stop(self) -> None:
        self.is_running = False
