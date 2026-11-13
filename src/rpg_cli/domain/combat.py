from dataclasses import dataclass

from rpg_cli.domain.character import Character


@dataclass(frozen=True)
class AttackResult:
    damage: int
    killed: bool


def attack(attacker: Character, defender: Character) -> AttackResult:
    if not attacker.is_alive:
        raise ValueError("attacker cannot be dead")

    if not defender.is_alive:
        raise ValueError("defender cannot be dead")

    if attacker is defender:
        raise ValueError("attacker cannot be the same character of defender")

    damage = max(1, attacker.attack - defender.defense)

    damage_taken = defender.take_damage(damage)
    killed = not defender.is_alive

    return AttackResult(damage=damage_taken, killed=killed)
