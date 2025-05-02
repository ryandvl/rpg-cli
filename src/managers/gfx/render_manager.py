from signal import SIGWINCH, signal

from config import MAX_FPS, MIN_SIZE
from src.globals import BOLD, TYPE_CHECKING, curses, hide_cursor, sleep
from src.utils.window import WindowUtil

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

    is_valid_size: bool = True

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

        self.console.load()
        self.console.success("Game started!")

        hide_cursor()
        signal(SIGWINCH, self.handle_resize)

        stdscr.nodelay(True)
        self.check_size()
        while self.game.is_running:
            self.update()
            sleep(1 / MAX_FPS)

    def get_size(self) -> tuple[int, int]:
        cols, rows = self.stdscr.getmaxyx()
        return rows, cols

    def check_size(self) -> bool:
        rows, cols = self.get_size()
        self.is_valid_size = rows >= MIN_SIZE[0] and cols >= MIN_SIZE[1]

        return self.is_valid_size

    def invalid_size(self) -> None:
        if self.is_valid_size:
            return

        stdscr = self.stdscr
        screen = WindowUtil(stdscr)
        gcp = self.get_color_pair

        screen.background(gcp(0, 26))
        screen.erase()

        lines, cols = screen.size()
        subwin = screen.sub_window(lines // 2, round(cols / 1.8), lines // 4, cols // 4)
        subwin_lines, _ = subwin.size()
        subwin.background(gcp(0, 10))
        subwin.add_string(
            "INVALID SIZE",
            color=gcp(16, 10) | BOLD,
            y=1,
            center=True,
        )

        subwin.add_string(
            f"Current size: {lines}, {cols}",
            x=subwin_lines // 2,
            y=3,
            center=True,
            color=gcp(0, 10) | BOLD,
        )

        min_w, min_h = MIN_SIZE
        subwin.add_string(
            f"Minimal size: {min_w}, {min_h}",
            x=subwin_lines // 2,
            y=4,
            center=True,
            color=gcp(0, 10) | BOLD,
        )

        subwin.add_string(
            " Change window size or ",
            x=subwin_lines // 2,
            y=6,
            color=gcp(1, 250),
            center=True,
        )

        subwin.add_string(
            " Press Q or F4 to quit ",
            x=subwin_lines // 2,
            y=7,
            color=gcp(1, 250),
            center=True,
        )

        screen.refresh()

    @staticmethod
    def handle_resize(signum, frame) -> None:
        stdscr, console = render.stdscr, render.console

        curses.endwin()
        stdscr.refresh()

        rows, cols = render.get_size()
        console.warn(f"Screen resized to: {rows}, {cols} (Forced Render)")
        curses.COLS = rows
        curses.LINES = cols
        render.check_size()

    def update(self) -> None:
        if not self.is_valid_size:
            self.keyboard.update()

            return self.invalid_size()

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
