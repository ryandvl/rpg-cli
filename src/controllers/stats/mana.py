from src.controllers import bar_controller
from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import space_string

class ManaOptions:
    mana: float
    max_mana: float

    def __init__(self, max_mana: float) -> None:
        self.mana = max_mana
        self.max_mana = max_mana


class ManaControl:
    '''
    Control the display to player and mobs mana
    '''
    mana: float
    max_mana: float
    isPlayer: bool = False

    def __init__(self, options: ManaOptions) -> None:
        self.mana = options.mana
        self.max_mana = options.max_mana

    def print(self) -> None:
        GameLogger.print(
            f' &black→ &cyan{space_string('Mana', 15)}' +
            bar_controller.createBar(self.mana, self.max_mana, 'cyan')
        )
