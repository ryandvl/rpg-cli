import curses


def hide_cursor() -> None:
    """
    Hides the cursor with curses
    """
    curses.curs_set(False)


def show_cursor() -> None:
    """
    Show the cursor with curses
    """
    curses.curs_set(True)
