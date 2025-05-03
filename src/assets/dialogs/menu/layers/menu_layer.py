from src.interfaces.layer_interface import LayerInterface


class MenuLayer(LayerInterface):
    name = "menu_layer"
    priority = 1

    def draw(self) -> None:
        screen = self.util

        lines, cols = screen.size()
        window = screen.sub_window_center(lines // 6, cols // 4)

        window.set_border(self.gcp(0, 0))
        window.add_string("GAME MENU", color=self.gcp(9, 255), x=1, y=1, center=True)
        window.background(self.gcp(0, 255))
