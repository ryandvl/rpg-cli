from config import VALID_DOWN_KEYS, VALID_SELECT_KEYS, VALID_UP_KEYS
from src.globals import BOLD, TYPE_CHECKING, curses
from src.interfaces.enum.position_enum import TitlePosition
from src.interfaces.layer_interface import LayerInterface
from src.interfaces.selection_interface import SelectionInterface
from src.utils.window import WindowUtil

if TYPE_CHECKING:
    from src.managers.game_manager import GameManager


def check_selection(window: curses.window, game: "GameManager", key: int | None):
    if game.selection is None:
        return

    selection = game.selection

    if key in VALID_UP_KEYS:
        selection.previous()
    elif key in VALID_DOWN_KEYS:
        selection.next()
    elif key in VALID_SELECT_KEYS:

        def close():
            game.dialogs.close("menu")

        id = selection.selected_id
        if id == "return":  # Return to Game
            close()
        elif id == "open-console":  # Open Console
            close()
            game.console.open()


class MenuLayer(LayerInterface):
    name = "menu_layer"
    priority = 1
    has_selection = True
    inputs = {"selection": check_selection}

    def load(self) -> None:
        selection = self.selection

        def render(
            window: WindowUtil, interface: SelectionInterface, is_selected: bool
        ):
            color = self.gcp(0, 235)

            if is_selected:
                color = self.gcp(235, 155)

            col = interface.num + 1
            lines, _ = window.size()

            window.fill(1, col, lines - 2, col, " ", color)
            window.add_string(interface.text, color, x=0, y=col, center=True)

        selection.set_render_option(render)
        selection.add_option("return", "Return to Game")
        selection.add_option("open-console", "Open console")

    def draw(self) -> None:
        screen = self.util
        selection = self.selection

        window = screen.sub_window_center(26, 5 + selection.max_selection)

        background = 235
        window.background(self.gcp(0, background))

        window.set_border(self.gcp(0, 0))
        window.set_title(
            " RPG CLI Menu ",
            color=self.gcp(119, background - 1) | BOLD,
            position=TitlePosition.TOP_CENTER,
        )

        selection.render(window)

        window.refresh()
