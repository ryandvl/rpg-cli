import pytest

from rpg_cli.domain.character import Character

# --- Class Creation ---


def test_hp_defaults_to_max_hp():
    hero = Character(name="Hero", max_hp=10)

    assert hero.hp == 10


def test_can_start_with_custom_hp():
    hero = Character(name="Hero", max_hp=10, hp=4)

    assert hero.hp == 4


@pytest.mark.parametrize("max_hp", [0, -5])
def test_non_positive_max_hp_raises(max_hp):
    with pytest.raises(ValueError):
        Character(name="Hero", max_hp=max_hp)


@pytest.mark.parametrize("hp", [-1, 11])
def test_hp_out_of_range_raises(hp):
    with pytest.raises(ValueError):
        Character(name="Hero", max_hp=10, hp=hp)


# --- Damage ---


def test_take_damage_reduces_hp():
    hero = Character(name="Hero", max_hp=10)

    dealt = hero.take_damage(3)

    assert hero.hp == 7
    assert dealt == 3


def test_take_damage_does_not_go_below_zero():
    hero = Character(name="Hero", max_hp=10, hp=3)

    dealt = hero.take_damage(999)

    assert hero.hp == 0
    assert dealt == 3
    assert not hero.is_alive


def test_negative_damage_raises():
    hero = Character(name="Hero", max_hp=10)

    with pytest.raises(ValueError):
        hero.take_damage(-1)


# --- Heal ---


def test_heal_increases_hp():
    hero = Character(name="Hero", max_hp=10, hp=5)

    healed = hero.heal(3)

    assert hero.hp == 8
    assert healed == 3


def test_heal_does_not_exceed_max_hp():
    hero = Character(name="Hero", max_hp=10, hp=9)

    healed = hero.heal(50)

    assert hero.hp == 10
    assert healed == 1


def test_negative_heal_raises():
    hero = Character(name="Hero", max_hp=10)

    with pytest.raises(ValueError):
        hero.heal(-1)


def test_heal_dead_character():
    hero = Character(name="Hero", max_hp=10)

    hero.take_damage(10)

    assert not hero.is_alive

    with pytest.raises(ValueError):
        hero.heal(1)


# --- HP ---


def test_is_alive_with_hp():
    hero = Character(name="Hero", max_hp=10, hp=1)

    assert hero.is_alive
