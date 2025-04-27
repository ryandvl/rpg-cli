from src.interfaces.layer_interface import LayerInterface


class LogsLayer(LayerInterface):
    name = "logs"
    priority = 1

    def draw(self) -> None:
        screen = self.util

        screen.clear()
        screen.background(self.gcp(0, 8))

        lines, cols = screen.size()
        logs_window = screen.sub_window(self.console, lines, int(cols // 1.05))
        logs_window.background(self.console.background)

        for log in self.console.logs:
            for message_part in log.message_parts:
                logs_window.add_string(message_part.message, message_part.color)

            logs_window.break_line()

        logs_window.refresh()
