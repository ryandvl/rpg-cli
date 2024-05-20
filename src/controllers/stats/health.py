from src.controllers import bar_controller
from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import space_string

class HealthOptions:
    health: float
    max_health: float

    def __init__(self, max_health: float) -> None:
        self.health = max_health
        self.max_health = max_health


class HealthControl:
    '''
    Control the display to player and mobs health
    '''
    health: float
    max_health: float
    isPlayer: bool = False

    def __init__(self, options: HealthOptions) -> None:
        self.health = options.health
        self.max_health = options.max_health

    def print(self) -> None:
        GameLogger.print(
            f' &black→ &magenta{space_string('Health', 15)}' +
            bar_controller.createBar(self.health, self.max_health, 'magenta')
        )
