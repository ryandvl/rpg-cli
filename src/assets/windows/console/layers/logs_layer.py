from src.globals import BOLD, TYPE_CHECKING, curses, get_char_key
from src.interfaces.layer_interface import LayerInterface
from src.utils.math import check_size

if TYPE_CHECKING:
    from src.managers.game_manager import GameManager


def check_move(window: curses.window, game: "GameManager", key: int | None):
    console = game.console
    keyboard = game.keyboard

    visible_lines = console.visible_lines
    start_line = console.start_line
    logs = console.logs

    if key == ord("q"):
        console.info(f"{console.visible_lines} {len(console.logs) + 1}")
        keyboard.should_render()
        return

    has_min_logs = len(logs) >= console.visible_lines
    if not has_min_logs:
        return

    jump_length = 22
    render = True
    if key in (curses.KEY_UP, curses.KEY_PPAGE):
        console.start_line = max(0, start_line - jump_length)
        console.sticked = False
    elif key in (curses.KEY_DOWN, curses.KEY_NPAGE):
        console.start_line = min(len(logs) - visible_lines, start_line + jump_length)
        console.sticked = False
    elif key == get_char_key("s"):
        console.sticked = not console.sticked
    else:
        render = False

    if render:
        keyboard.should_render()


class LogsLayer(LayerInterface):
    name = "logs"
    priority = 1
    inputs = {"move": check_move}

    def draw(self) -> None:
        screen = self.util
        console = self.console

        logs = console.logs

        screen.erase()

        lines, cols = screen.max_size()
        gap_size = check_size(round(cols // 1.05), 0, cols - 3)

        # Logs
        logs_window = screen.sub_window(lines, gap_size)
        logs_size = logs_window.size()
        console.visible_lines = logs_window.size()[1]

        max_logs = max(0, len(logs) - console.visible_lines)
        if console.sticked:
            console.start_line = max_logs

        logs_window.background(console.background)

        visible_lines = console.visible_lines
        start_line = console.start_line

        for i in range(visible_lines):
            index = start_line + i
            if not (0 <= index < len(logs)):
                continue

            log = logs[index]

            logs_window.move(0, i)
            for message_part in log.message_parts:
                logs_window.add_string(message_part.message, message_part.color)

        logs_window.refresh()

        # Footer
        footer_size_cols = cols - logs_size[1]
        footer_window = screen.sub_window(lines, footer_size_cols, 0, logs_size[1])

        footer_window.background(self.gcp(0, 233))

        footer_middle = footer_size_cols // 2

        footer_window.add_string(
            string=" LEAVE ",
            x=lines - 10,
            y=footer_middle,
            center=True,
            color=self.gcp(0, 9) | BOLD,
        )
        footer_window.add_string(string=" <ESC> ", color=self.gcp(17, 8) | BOLD)

        footer_window.refresh()
