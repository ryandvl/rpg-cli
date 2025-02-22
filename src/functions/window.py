import curses

def write(window: curses.window, string: str, x: int, y: int, attr: int = 0) -> None:
    window.move(y, x)
    window.addstr(string, attr)

def top_left_title(window: curses.window, title: str, attr: int) -> None:
    write(window, title, 1, 0, attr)

def top_center_title(window: curses.window, title: str, attr: int) -> None:
    _, width = window.getmaxyx()

    write(window, title, (width - len(title)) // 2, 0, attr)

def top_right_title(window: curses.window, title: str, attr: int) -> None:
    _, width = window.getmaxyx()

    write(window, title, (width - len(title)) - 1, 0, attr)

def attr_on(window: curses.window, attr: int) -> None:
    window.attron(attr)

def attr_off(window: curses.window, attr: int) -> None:
    window.attroff(attr)

def set_border(window: curses.window, attr: int, hide: bool = False) -> None:
    attr_on(window, attr)

    window.border(' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ') if hide else window.border()

    attr_off(window, attr)
