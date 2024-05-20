from src.controllers.stats.energy import EnergyControl, EnergyOptions
from src.controllers.stats.health import HealthControl, HealthOptions
from src.controllers.stats.mana import ManaControl, ManaOptions
from src.controllers.stats.shield import ShieldControl, ShieldOptions

class StatsOptions:
    max_health: float = 100
    max_energy: float = 100
    max_mana: float = 100
    max_shield: float = 100

class StatsControl:
    health: HealthControl
    energy: EnergyControl
    mana: ManaControl
    shield: ShieldControl
    
    def __init__(self, options: StatsOptions) -> None:
        health_options = HealthOptions(options.max_health)
        self.health = HealthControl(health_options)

        energy_options = EnergyOptions(options.max_energy)
        self.energy = EnergyControl(energy_options)

        mana_options = ManaOptions(options.max_mana)
        self.mana = ManaControl(mana_options)

        shield_options = ShieldOptions(options.max_shield)
        self.shield = ShieldControl(shield_options)
        pass

    def print_minimal(self) -> None:
        self.health.print()
        self.energy.print()
        self.mana.print()
        self.shield.print()

    def print_all(self) -> None:
        self.print_minimal()
        