from src.globals import *

# ===

MAX_FPS = 60

MIN_SIZE = [64, 20]  # LINES, COLS

CONSOLE_WINDOW_NAME = "console"  # NOT CHANGE THIS
CONSOLE_BACKGROUND = [16, 17]  # FOREGROUND, BACKGROUND

DARK_GRAY = "$9,17$"

VALID_UP_KEYS = (
    curses.KEY_UP,
    curses.KEY_PPAGE,
    get_char_key("w"),
    # Vim based
    get_char_key("k"),
    get_char_key("p"),
    get_char_key("P"),
)
VALID_DOWN_KEYS = (
    curses.KEY_DOWN,
    curses.KEY_NPAGE,
    get_char_key("s"),
    # Vim based
    get_char_key("j"),
    get_char_key("n"),
    get_char_key("N"),
)
VALID_SELECT_KEYS = (
    get_named_key("space"),
    curses.KEY_ENTER,
    ord("\n"),  # For Unix-like OS
    ord("\r"),  # For Windows, etc.
)
