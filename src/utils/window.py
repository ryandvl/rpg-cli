import curses


def create_win(
    self, lines: int = 1, columns: int = 1, x: int = 0, y: int = 0
) -> curses.window:
    return curses.newwin(lines, columns, x, y)


class WindowUtil:
    window: curses.window

    def __init__(self, window: curses.window) -> None:
        self.window = window

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
        temp,
        lines: int | None,
        cols: int | None,
        x: int = 0,
        y: int = 0,
    ) -> "WindowUtil":
        max_lines, max_cols = self.size()

        lines = max_lines if lines is None else lines
        cols = max_cols if cols is None else cols

        def check_size(n: int, min_n: int, max_n: int) -> int:
            return max(min_n, min(n, max_n))

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
        return curses.COLS, curses.LINES

    def refresh(self) -> None:
        self.window.refresh()
