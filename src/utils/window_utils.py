import curses

def write(window: curses.window, string: str, x: int, y: int, attr: int = 0):
    window.move(y, x)
    window.addstr(string, attr)

def top_left_title(window: curses.window, title: str, attr: int):
    write(window, title, 1, 0, attr)

def top_center_title(window: curses.window, title: str, attr: int):
    _, width = window.getmaxyx()

    write(window, title, (width - len(title)) // 2, 0, attr)

def top_right_title(window: curses.window, title: str, attr: int):
    _, width = window.getmaxyx()

    write(window, title, (width - len(title)) - 1, 0, attr)

def attr_on(window: curses.window, attr: int):
    window.attron(attr)

def attr_off(window: curses.window, attr: int):
    window.attroff(attr)

def set_border(window: curses.window, attr: int, hide: bool = False):
    attr_on(window, attr)
    if hide:
        window.border(' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')
    else:
        window.border()
    attr_off(window, attr)
