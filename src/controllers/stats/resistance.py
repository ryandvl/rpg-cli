from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import equalize_string, insert_string, space_string

class ResistanceOptions:
    resistance: int
    max_resistance: int


class ResistanceControl:
    '''
    Control the display to player and mobs resistance
    '''
    resistance: float
    max_resistance: float
    isPlayer: bool = False

    def __init__(self, options: ResistanceOptions) -> None:
        self.resistance = options.resistance
        self.max_resistance = options.max_resistance

    def getMessage(self) -> str:
        resistance_size = int(
            (self.resistance / self.max_resistance) * 20
        )

        resistanceBar = insert_string(
            equalize_string(f'{self.resistance}/{self.max_resistance}', 20), "&reset", resistance_size
        )

        return f'&reset&black[&bg_white' +\
            resistanceBar +\
            '&reset&black]&reset'

    def print(self) -> None:
        GameLogger.print(
            f'&black⊢ &bold&white{space_string('ARMOR', 10)}' +
            self.getMessage()
        )
