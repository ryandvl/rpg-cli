from src.functions.window import (
    create_win,
    set_border,
)
from src.interfaces.layer_interface import (
    LayerInterface,
)


class GameMenu_MenuLayer(LayerInterface):
    name = "menu"
    priority = 1

    def render(
        self,
    ) -> None:
        window = create_win(
            lines=12,
            columns=30,
            x=4,
            y=40,
        )

        set_border(
            window,
        )

        window.refresh()
