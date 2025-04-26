from src.interfaces.layer_interface import LayerInterface


class MenuLayer(LayerInterface):
    name = "menu"
    priority = 1

    def draw(self) -> None:
        self.window.addch("a")
        pass
