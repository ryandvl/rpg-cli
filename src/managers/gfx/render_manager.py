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

    should_render: bool = True
    should_clear: bool = False

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

    @staticmethod
    def handle_resize(signum, frame) -> None:
        stdscr, console = render.stdscr, render.console

        curses.endwin()
        stdscr.refresh()

        cols, rows = stdscr.getmaxyx()
        console.warn(f"Screen resized to: {rows}, {cols} (Forced Render)")
        curses.COLS = rows
        curses.LINES = cols

        render.update(True)

    def update(self, forced: bool = False) -> None:
        if render.should_clear:
            render.should_clear = False

        if forced or self.should_render:
            render.should_clear = forced

            self.windows.render(render.should_clear)
            self.dialogs.render(render.should_clear)

            self.should_render = False

        self.keyboard.update(forced)

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
