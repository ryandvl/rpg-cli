from src.controllers.stats.energy import EnergyControl, EnergyOptions
from src.controllers.stats.health import HealthControl, HealthOptions
from src.controllers.stats.mana import ManaControl, ManaOptions
from src.controllers.stats.resistance import ResistanceControl, ResistanceOptions

if __name__ == '__main__':
    healthOptions = HealthOptions()
    healthOptions.health = 20
    healthOptions.max_health = 100

    healthControl = HealthControl(healthOptions)
    healthControl.print()


    energyOptions = EnergyOptions()
    energyOptions.energy = 100
    energyOptions.max_energy = 100

    energyControl = EnergyControl(energyOptions)
    energyControl.print()


    manaOptions = ManaOptions()
    manaOptions.mana = 50
    manaOptions.max_mana = 100

    manaControl = ManaControl(manaOptions)
    manaControl.print()


    resistanceOptions = ResistanceOptions()
    resistanceOptions.resistance = 35
    resistanceOptions.max_resistance = 100

    resistanceControl = ResistanceControl(resistanceOptions)
    resistanceControl.print()
