from dataclasses import dataclass

from rpg_cli.domain.character import Character


@dataclass(frozen=True)
class MobTemplate:
    name: str
    max_hp: int
    attack: int
    defense: int
    crit_chance: float = 0.0

    def spawn(self) -> Character:
        return Character(
            name=self.name,
            max_hp=self.max_hp,
            attack=self.attack,
            defense=self.defense,
            crit_chance=self.crit_chance,
        )


SLIME = MobTemplate(
    name="Slime",
    max_hp=6,
    attack=2,
    defense=0,
)

GOBLIN = MobTemplate(
    name="Goblin",
    max_hp=12,
    attack=4,
    defense=1,
    crit_chance=0.1,
)

WOLF = MobTemplate(
    name="Wolf",
    max_hp=10,
    attack=7,
    defense=0,
    crit_chance=0.25,
)
