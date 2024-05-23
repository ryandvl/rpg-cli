from src.controllers import bar_controller
from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import space_string

class EnergyOptions:
    energy: float
    max_energy: float

    def __init__(self, max_energy: float) -> None:
        self.energy = max_energy
        self.max_energy = max_energy


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

    def print(self) -> None:
        GameLogger.print(
            f' &black→ &yellow{space_string('Energy', 10)}' +
            bar_controller.createBar(self.energy, self.max_energy, 'yellow')
        )
