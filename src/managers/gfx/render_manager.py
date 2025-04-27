from signal import SIGWINCH, signal

from src.globals import TYPE_CHECKING, curses, hide_cursor

if TYPE_CHECKING:
    from ..console_manager import ConsoleManager
    from ..game_manager import GameManager
    from ..keyboard_manager import KeyboardManager
    from .dialogs_manager import DialogsManager
    from .windows_manager import WindowsManager


class RenderManager:
    game: "GameManager"
    console: "ConsoleManager"
    windows: "WindowsManager"
    keyboard: "KeyboardManager"
    dialogs: "DialogsManager"

    color_pairs: dict[str, int] = dict()
    stdscr: curses.window

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.console = game.console
        self.keyboard = game.keyboard
        self.windows = game.windows
        self.dialogs = game.dialogs

    def wrapper(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr

        global render
        render = self

        curses.start_color()
        curses.use_default_colors()

        self.windows.load_default(stdscr)
        self.dialogs.load()

        self.console.load()
        self.console.success("Game started!")

        hide_cursor()
        signal(SIGWINCH, self.handle_resize)

        while self.game.is_running:
            self.update()
            self.console.info("render")

    @staticmethod
    def handle_resize(signum, frame) -> None:
        stdscr, console = render.stdscr, render.console

        curses.endwin()
        stdscr.refresh()

        rows, cols = stdscr.getmaxyx()
        console.info(f"Screen resized to: {rows}x{cols}")

    def update(self) -> None:
        self.windows.render()
        self.dialogs.render()

        self.keyboard.update()

    def create_color_pair(self, foreground: int, background: int) -> int:
        newID: int = len(self.color_pairs.keys()) + 1
        name = f"{foreground} {background}"

        curses.init_pair(newID, foreground, background)
        self.color_pairs[name] = curses.color_pair(newID)

        return self.color_pairs[name]

    def get_color_pair(self, foreground: int = 0, background: int = 0) -> int:
        foreground = foreground - 1
        background = background - 1

        name = f"{foreground} {background}"

        if not self.color_pairs.get(name):
            return self.create_color_pair(foreground, background)

        return self.color_pairs[name]
