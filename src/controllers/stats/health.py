from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import equalize_string, insert_string, space_string

class HealthOptions:
    health: int
    max_health: int


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

    def getMessage(self) -> str:
        color = 'bg_green' if self.isPlayer else 'bg_magenta'

        health_size = int(
            (self.health / self.max_health) * 20
        )

        healthBar = insert_string(
            equalize_string(f'{self.health}/{self.max_health}', 20), "&reset", health_size
        )

        return f'&reset&black[&{color}' +\
            healthBar +\
            '&reset&black]&reset'

    def print(self) -> None:
        GameLogger.print(
            f'&black⊢ &bold&magenta{space_string('HEALTH', 10)}' +
            self.getMessage()
        )
