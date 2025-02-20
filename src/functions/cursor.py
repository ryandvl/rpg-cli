import curses

def hide_cursor() -> None:
    curses.curs_set(False)

def show_cursor() -> None:
    curses.curs_set(True)
