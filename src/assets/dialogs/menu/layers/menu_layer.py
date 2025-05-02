from src.interfaces.layer_interface import LayerInterface


class MenuLayer(LayerInterface):
    name = "menu_layer"
    priority = 1

    def draw(self) -> None:
        self.window.addstr("test")
        self.util.background(self.gcp(0, 237))
