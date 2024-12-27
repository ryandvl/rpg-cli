import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.controllers.keyboard_controller import KeyboardController

def test(window: curses.window, keyboard_controller: 'KeyboardController', key_code: int | None):
    window.addstr(6, 30, str(key_code))

    if key_code == ord('q'):
        window.addstr(5, 30, 'click Q')
    elif key_code == ord('w'):
        window.addstr(5, 30, 'click W')

def create_keyboard_inputs(k: 'KeyboardController'):
    c = k.create_input

    c(name='teste', func=test)

