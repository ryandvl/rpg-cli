from src.interfaces.layer_interface import LayerInterface


class LogsLayer(LayerInterface):
    name = "logs"
    priority = 1

    def draw(self) -> None:
        for log in self.game.console.logs:
            for message_part in log.message_parts:
                self.window.addstr(message_part.message, message_part.color)

            self.window.addch("\n")
