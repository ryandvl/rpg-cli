from src.interfaces.layer_interface import LayerInterface


class LogsLayer(LayerInterface):
    name = "logs"
    priority = 1

    def draw(self) -> None:
        pass
