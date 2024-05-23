from src.controllers import bar_controller
from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import space_string

class ShieldOptions:
    shield: float
    max_shield: float

    def __init__(self, max_shield: float) -> None:
        self.shield = max_shield
        self.max_shield = max_shield


class ShieldControl:
    '''
    Control the display to player and mobs shield
    '''
    shield: float
    max_shield: float
    isPlayer: bool = False

    def __init__(self, options: ShieldOptions) -> None:
        self.shield = options.shield
        self.max_shield = options.max_shield

    def print(self) -> None:
        GameLogger.print(
            f' &black→ &blue{space_string('Shield', 10)}' +
            bar_controller.createBar(self.shield, self.max_shield, 'blue')
        )
