from src.globals import TYPE_CHECKING, curses, get_char_key
from src.interfaces.layer_interface import LayerInterface

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

    render = True
    if key == curses.KEY_UP:
        console.start_line = max(0, start_line - 1)
        console.sticked = False
        if console.start_line == 0:
            render = False
    elif key == curses.KEY_DOWN:
        console.start_line = min(len(logs) - visible_lines, start_line + 1)
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

        screen.background(self.gcp(0, 233))
        screen.clear()

        lines, cols = screen.max_size()
        logs_window = screen.sub_window(lines, int(cols // 1.05))
        console.visible_lines = logs_window.size()[1]

        max_logs = max(0, len(logs) - console.visible_lines)
        if console.sticked:
            console.start_line = max_logs

        logs_window.background(console.background)

        visible_lines = console.visible_lines
        start_line = console.start_line

        # add "sticked" string

        for i in range(visible_lines):
            index = start_line + i
            if not (0 <= index < len(logs)):
                continue

            log = logs[index]

            logs_window.move(0, i)
            for message_part in log.message_parts:
                logs_window.add_string(message_part.message, message_part.color)

        logs_window.refresh()
