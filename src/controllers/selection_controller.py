from src.globals import TYPE_CHECKING, Callable, in_size
from src.interfaces.selection_interface import SelectionInterface

if TYPE_CHECKING:
    from src.managers.game_manager import GameManager
    from src.utils.window import WindowUtil


class SelectionController:
    game: "GameManager"

    selections: list[SelectionInterface] = list()

    selected: int = 0
    selected_id: str = ""
    max_selection: int = 0

    render_option: Callable[["WindowUtil", SelectionInterface, bool], None]

    def __init__(self, game: "GameManager") -> None:
        self.game = game

    def set_render_option(self, func: Callable) -> None:
        self.render_option = func

    def is_selected(self, option: int) -> bool:
        return self.selected == option

    def add_option(self, id: str, option: str, render: Callable | None = None) -> None:
        interface = SelectionInterface()

        interface.id = id
        interface.text = option
        interface.render = render if render is not None else self.render_option
        interface.num = len(self.selections) + 1

        self.selections.append(interface)

        self.selected = 1 if self.selected == 0 else self.selected
        self.check_name()
        self.max_selection += 1

    def focus(self):
        self.game.selection = self

    def render(self, window: "WindowUtil") -> None:
        for selection in self.selections:
            selection.render(window, selection, self.is_selected(selection.num))

    def previous(self, quantity: int = 1) -> bool:
        old_selected = self.selected

        self.selected = max(self.selected - quantity, 1)
        self.check_name()

        return self.selected < old_selected

    def next(self, quantity: int = 1) -> bool:
        old_selected = self.selected

        self.selected = min(self.selected + quantity, self.max_selection)
        self.check_name()

        return self.selected > old_selected

    def jump(self, selection: int) -> bool:
        can_jump = in_size(selection, 1, self.max_selection)

        if can_jump:
            self.selected = selection
            self.check_name()

        return can_jump

    def reset(self) -> None:
        self.selected = 0
        self.max_selection = 0

    def check_name(self) -> None:
        try:
            id = self.selections[self.selected - 1].id  # Array starts from 0
        except IndexError:
            return

        self.selected_id = id
