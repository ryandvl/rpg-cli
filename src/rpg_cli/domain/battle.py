import random
from dataclasses import dataclass

from rpg_cli.domain.character import Character
from rpg_cli.domain.combat import AttackResult, Rng, attack


@dataclass(frozen=True)
class Turn:
    attacker: str
    defender: str
    result: AttackResult


@dataclass(frozen=True)
class BattleResult:
    winner: str
    turns: tuple[Turn, ...]


def fight(hero: Character, enemy: Character, rng: Rng | None = None) -> BattleResult:
    rng = random.Random() if rng is None else rng
    turns: list[Turn] = []
    winner = hero.name

    while True:
        # Hero turn
        result = attack(attacker=hero, defender=enemy, rng=rng)
        turns.append(Turn(attacker=hero.name, defender=enemy.name, result=result))

        if not enemy.is_alive:
            break

        # Enemy turn
        result = attack(attacker=enemy, defender=hero, rng=rng)
        turns.append(Turn(attacker=enemy.name, defender=hero.name, result=result))

        if not hero.is_alive:
            winner = enemy.name
            break

    return BattleResult(winner=winner, turns=tuple(turns))
