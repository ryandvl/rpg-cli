from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import equalize_string, insert_string, space_string

class EnergyOptions:
    energy: int
    max_energy: int


class EnergyControl:
    '''
    Control the display to player and mobs energy
    '''
    energy: float
    max_energy: float
    isPlayer: bool = False

    def __init__(self, options: EnergyOptions) -> None:
        self.energy = options.energy
        self.max_energy = options.max_energy

    def getMessage(self) -> str:
        energy_size = int(
            (self.energy / self.max_energy) * 20
        )

        energyBar = insert_string(
            equalize_string(f'{self.energy}/{self.max_energy}', 20), "&reset", energy_size
        )

        return f'&reset&black[&bg_yellow' +\
            energyBar +\
            '&reset&black]&reset'

    def print(self) -> None:
        GameLogger.print(
            f'&black⊢ &bold&yellow{space_string('ENERGY', 10)}' +
            self.getMessage()
        )
