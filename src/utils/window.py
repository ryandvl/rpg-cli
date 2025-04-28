import curses

from .math import check_size


def create_win(
    self, lines: int = 1, columns: int = 1, x: int = 0, y: int = 0
) -> curses.window:
    return curses.newwin(lines, columns, x, y)


class WindowUtil:
    window: curses.window

    def __init__(self, window: curses.window) -> None:
        self.window = window

    def move(self, x: int, y: int) -> bool:
        try:
            max_lines, max_cols = self.max_size()

            self.window.move(
                check_size(y, 0, max_lines),
                check_size(x, 0, max_cols),
            )
        except Exception:
            return False

        return True

    def add_string(self, string: str, color: int = 0) -> bool:
        try:
            self.window.addstr(string, color)
        except Exception:
            return False

        return True

    def add_char(self, char: str, color: int = 0) -> bool:
        try:
            self.window.addch(char, color)
        except Exception:
            return False

        return True

    def break_line(self) -> bool:
        return self.add_char("\n")

    def clear(self) -> None:
        self.window.clear()

    def background(self, color: int = 0, attr: int = 0) -> None:
        self.window.bkgd(color, attr)

    def sub_window(
        self,
        lines: int | None,
        cols: int | None,
        x: int = 0,
        y: int = 0,
    ) -> "WindowUtil":
        max_lines, max_cols = self.max_size()

        lines = max_lines if lines is None else lines
        cols = max_cols if cols is None else cols

        subwin = self.window.subwin(
            check_size(cols, 1, max_cols),
            check_size(lines, 1, max_lines),
            check_size(y, 0, max_lines),
            check_size(x, 0, max_cols),
        )

        return WindowUtil(subwin)

    def write(self, string: str, x: int, y: int, attr: int = 0) -> None:
        self.window.move(y, x)
        self.window.addstr(string, attr)

    def top_left_title(self, title: str, attr: int) -> None:
        self.write(title, 1, 0, attr)

    def top_center_title(self, title: str, attr: int) -> None:
        _, width = self.window.getmaxyx()

        self.write(title, (width - len(title)) // 2, 0, attr)

    def top_right_title(self, title: str, attr: int) -> None:
        _, width = self.window.getmaxyx()

        self.write(title, (width - len(title)) - 1, 0, attr)

    def attr_on(self, attr: int) -> None:
        self.window.attron(attr)

    def attr_off(self, attr: int) -> None:
        self.window.attroff(attr)

    def set_border(self, attr: int, hide: bool = False) -> None:
        self.attr_on(attr)

        self.window.border(
            " ", " ", " ", " ", " ", " ", " ", " "
        ) if hide else self.window.border()

        self.attr_off(attr)

    def size(self) -> tuple[int, int]:
        cols, lines = self.window.getmaxyx()
        return lines, cols

    def max_size(self) -> tuple[int, int]:
        return curses.COLS, curses.LINES

    def fill(
        self, y1: int, x1: int, y2: int, x2: int, char: str, attr: int = 0
    ) -> None:
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("The argument 'char' is not a char.")

        max_y, max_x = self.window.getmaxyx()

        y1 = max(0, min(y1, max_y - 1))
        x1 = max(0, min(x1, max_x - 1))
        y2 = max(0, min(y2, max_y - 1))
        x2 = max(0, min(x2, max_x - 1))

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.window.addch(y, x, char, attr)

        self.window.noutrefresh()

    def refresh(self) -> None:
        self.window.refresh()
