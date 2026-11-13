from dataclasses import dataclass


@dataclass(init=False)
class Character:
    name: str
    max_hp: int
    hp: int

    attack: int
    defense: int

    def __init__(
        self,
        name: str,
        max_hp: int,
        hp: int | None = None,
        attack: int = 0,
        defense: int = 0,
    ) -> None:
        if max_hp <= 0:
            raise ValueError("max_hp must be positive")

        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp if hp is None else hp

        self.attack = attack
        self.defense = defense

        if self.attack < 0:
            raise ValueError("attack must not be negative")

        if self.defense < 0:
            raise ValueError("defense must not be negative")

        if not 0 <= self.hp <= self.max_hp:
            raise ValueError("hp must be between 0 and max_hp")

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must not be negative")

        if not self.is_alive:
            raise ValueError("cannot heal a dead character")

        before = self.hp
        self.hp = min(self.hp + amount, self.max_hp)

        return self.hp - before

    def take_damage(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must not be negative")

        if not self.is_alive:
            raise ValueError("cannot damage a dead character")

        before = self.hp
        self.hp = max(self.hp - amount, 0)

        return before - self.hp
