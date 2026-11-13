import pytest

from rpg_cli.domain.character import Character
from rpg_cli.domain.combat import attack

# --- Damage ---


def test_damage_is_attack_minus_defense():
    hero = Character(name="Hero", max_hp=20, attack=7)
    goblin = Character(name="Goblin", max_hp=10, defense=2)

    result = attack(hero, goblin)

    assert result.damage == 5
    assert goblin.hp == 5


@pytest.mark.parametrize("defense", [5, 50])
def test_damage_is_at_least_one(defense):
    hero = Character(name="Hero", max_hp=20, attack=5)
    goblin = Character(name="Goblin", max_hp=10, defense=defense)

    result = attack(hero, goblin)

    assert result.damage == 1
    assert goblin.hp == 9


def test_damage_does_not_exceed_remaining_hp():
    hero = Character(name="Hero", max_hp=20, attack=10)
    goblin = Character(name="Goblin", max_hp=10, hp=2)

    result = attack(hero, goblin)

    assert result.damage == 2
    assert goblin.hp == 0


# --- Killed ---


def test_killed_when_defender_dies():
    hero = Character(name="Hero", max_hp=20, attack=10)
    goblin = Character(name="Goblin", max_hp=10, hp=2)

    result = attack(hero, goblin)

    assert result.killed
    assert not goblin.is_alive


def test_not_killed_when_defender_survives():
    hero = Character(name="Hero", max_hp=20, attack=3)
    goblin = Character(name="Goblin", max_hp=10)

    result = attack(hero, goblin)

    assert not result.killed
    assert goblin.is_alive


# --- Rules ---


def test_dead_attacker_raises():
    hero = Character(name="Hero", max_hp=20, hp=0, attack=5)
    goblin = Character(name="Goblin", max_hp=10)

    with pytest.raises(ValueError, match="attacker cannot be dead"):
        attack(hero, goblin)


def test_dead_defender_raises():
    hero = Character(name="Hero", max_hp=20, attack=5)
    goblin = Character(name="Goblin", max_hp=10, hp=0)

    with pytest.raises(ValueError, match="defender cannot be dead"):
        attack(hero, goblin)


def test_attacking_itself_raises():
    hero = Character(name="Hero", max_hp=20, attack=5)

    with pytest.raises(ValueError, match="attacker cannot be the same"):
        attack(hero, hero)


def test_equal_characters_can_fight():
    goblin1 = Character(name="Goblin", max_hp=10, attack=3)
    goblin2 = Character(name="Goblin", max_hp=10, attack=3)

    assert goblin1 == goblin2

    result = attack(goblin1, goblin2)

    assert result.damage == 3
    assert goblin2.hp == 7
    assert goblin1.hp == 10
