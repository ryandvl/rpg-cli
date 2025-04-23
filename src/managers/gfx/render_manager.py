from src.globals import TYPE_CHECKING, curses, hide_cursor

if TYPE_CHECKING:
    from ..game_manager import GameManager
    from ..keyboard_manager import KeyboardManager
    from .windows_manager import WindowsManager


class RenderManager:
    game: "GameManager"
    windows: "WindowsManager"
    keyboard: "KeyboardManager"

    color_pairs: dict[str, int] = dict()

    def setup(self, game: "GameManager") -> None:
        self.game = game
        self.keyboard = game.keyboard
        self.windows = game.windows

    def wrapper(self, window: curses.window) -> None:
        curses.start_color()
        curses.use_default_colors()

        self.windows.load_default(window)

        hide_cursor()

        self.update()
        while self.game.is_running:
            self.update()

    def update(self) -> None:
        if layer := self.windows.window.layer:
            layer.render()

        self.windows.window.win.refresh()

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
