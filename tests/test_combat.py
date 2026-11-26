import random

import pytest
from fakes import FakeRandom

from rpg_cli.domain.character import Character
from rpg_cli.domain.combat import attack

# --- Damage ---


def test_damage_is_attack_minus_defense():
    hero = Character(name="Hero", max_hp=20, attack=7)
    goblin = Character(name="Goblin", max_hp=10, defense=2)

    result = attack(hero, goblin, rng=FakeRandom())

    assert result.damage == 5
    assert goblin.hp == 5


@pytest.mark.parametrize("defense", [5, 50])
def test_damage_is_at_least_one(defense):
    hero = Character(name="Hero", max_hp=20, attack=5)
    goblin = Character(name="Goblin", max_hp=10, defense=defense)

    result = attack(hero, goblin, rng=FakeRandom())

    assert result.damage == 1
    assert goblin.hp == 9


def test_damage_does_not_exceed_remaining_hp():
    hero = Character(name="Hero", max_hp=20, attack=10)
    goblin = Character(name="Goblin", max_hp=10, hp=2)

    result = attack(hero, goblin, rng=FakeRandom())

    assert result.damage == 2
    assert goblin.hp == 0


# --- Variance ---


@pytest.mark.parametrize(("variance", "expected"), [(0.8, 6), (1.2, 10)])
def test_variance_limits(variance, expected):
    hero = Character(name="Hero", max_hp=20, attack=10)
    goblin = Character(name="Goblin", max_hp=50, defense=2)

    result = attack(hero, goblin, rng=FakeRandom(variance=variance))

    assert result.damage == expected


def test_damage_is_at_least_one_with_low_variance():
    hero = Character(name="Hero", max_hp=20, attack=3)
    goblin = Character(name="Goblin", max_hp=10, defense=3)

    result = attack(hero, goblin, rng=FakeRandom(variance=0.8))

    assert result.damage == 1


def test_seeded_damage_stays_in_range():
    rng = random.Random(42)
    hero = Character(name="Hero", max_hp=20, attack=10)
    goblin = Character(name="Goblin", max_hp=1000, defense=2)

    for _ in range(100):
        result = attack(hero, goblin, rng=rng)

        assert 6 <= result.damage <= 10
        assert not result.critical


# --- Critical ---


def test_critical_doubles_damage_before_defense():
    hero = Character(name="Hero", max_hp=20, attack=7, crit_chance=0.5)
    goblin = Character(name="Goblin", max_hp=50, defense=2)

    result = attack(hero, goblin, rng=FakeRandom(roll=0.1))

    assert result.critical
    assert result.damage == 12


def test_roll_above_crit_chance_is_not_critical():
    hero = Character(name="Hero", max_hp=20, attack=7, crit_chance=0.5)
    goblin = Character(name="Goblin", max_hp=50, defense=2)

    result = attack(hero, goblin, rng=FakeRandom(roll=0.6))

    assert not result.critical
    assert result.damage == 5


def test_full_crit_chance_always_crits():
    hero = Character(name="Hero", max_hp=20, attack=7, crit_chance=1.0)
    goblin = Character(name="Goblin", max_hp=50)

    result = attack(hero, goblin, rng=FakeRandom())

    assert result.critical


def test_zero_crit_chance_never_crits():
    hero = Character(name="Hero", max_hp=20, attack=7)
    goblin = Character(name="Goblin", max_hp=50)

    result = attack(hero, goblin, rng=FakeRandom(roll=0.0))

    assert not result.critical


# --- Killed ---


def test_killed_when_defender_dies():
    hero = Character(name="Hero", max_hp=20, attack=10)
    goblin = Character(name="Goblin", max_hp=10, hp=2)

    result = attack(hero, goblin, rng=FakeRandom())

    assert result.killed
    assert not goblin.is_alive


def test_not_killed_when_defender_survives():
    hero = Character(name="Hero", max_hp=20, attack=3)
    goblin = Character(name="Goblin", max_hp=10)

    result = attack(hero, goblin, rng=FakeRandom())

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

    result = attack(goblin1, goblin2, rng=FakeRandom())

    assert result.damage == 3
    assert goblin2.hp == 7
    assert goblin1.hp == 10
