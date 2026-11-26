import random
from dataclasses import dataclass
from typing import Protocol

from rpg_cli.domain.character import Character


class Rng(Protocol):
    def uniform(self, a: float, b: float) -> float: ...
    def random(self) -> float: ...


@dataclass(frozen=True)
class AttackResult:
    damage: int
    killed: bool
    critical: bool


def attack(
    attacker: Character, defender: Character, rng: Rng | None = None
) -> AttackResult:
    if not attacker.is_alive:
        raise ValueError("attacker cannot be dead")

    if not defender.is_alive:
        raise ValueError("defender cannot be dead")

    if attacker is defender:
        raise ValueError("attacker cannot be the same character of defender")

    rng = random.Random() if rng is None else rng

    base = attacker.attack * rng.uniform(0.8, 1.2)
    critical = rng.random() < attacker.crit_chance

    if critical:
        base *= 2

    damage = max(1, round(base) - defender.defense)
    damage_taken = defender.take_damage(damage)
    killed = not defender.is_alive

    return AttackResult(damage=damage_taken, killed=killed, critical=critical)
