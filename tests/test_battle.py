import random

import pytest

from fakes import FakeRandom
from rpg_cli.domain.battle import fight
from rpg_cli.domain.character import Character
from rpg_cli.domain.mobs import GOBLIN, SLIME

# --- Winner ---


def test_strong_hero_wins_in_one_turn():
    hero = Character(name="Hero", max_hp=30, attack=20)
    slime = SLIME.spawn()

    result = fight(hero, slime, rng=FakeRandom())

    assert result.winner == "Hero"
    assert len(result.turns) == 1
    assert not slime.is_alive


def test_weak_hero_loses():
    # Herói tira 1 por golpe (dano mínimo); o inimigo mata em 1 golpe.
    hero = Character(name="Hero", max_hp=5, attack=1)
    ogre = Character(name="Ogre", max_hp=50, attack=10)

    result = fight(hero, ogre, rng=FakeRandom())

    assert result.winner == "Ogre"
    assert len(result.turns) == 2
    assert not hero.is_alive
    assert ogre.hp == 49


# --- Turns ---


def test_multi_turn_battle_alternates_attackers():
    # Herói: 4 de dano por golpe -> slime 10 -> 6 -> 2 -> 0 (3 golpes).
    # Slime: ataca entre os golpes do herói (2 vezes).
    hero = Character(name="Hero", max_hp=30, attack=4)
    slime = Character(name="Slime", max_hp=10, attack=2)

    result = fight(hero, slime, rng=FakeRandom())

    attackers = [turn.attacker for turn in result.turns]
    defenders = [turn.defender for turn in result.turns]

    assert attackers == ["Hero", "Slime", "Hero", "Slime", "Hero"]
    assert defenders == ["Slime", "Hero", "Slime", "Hero", "Slime"]


def test_hero_keeps_damage_after_battle():
    hero = Character(name="Hero", max_hp=30, attack=4)
    slime = Character(name="Slime", max_hp=10, attack=2)

    fight(hero, slime, rng=FakeRandom())

    assert hero.hp == 26


def test_only_last_turn_kills():
    hero = Character(name="Hero", max_hp=30, attack=4)
    slime = Character(name="Slime", max_hp=10, attack=2)

    result = fight(hero, slime, rng=FakeRandom())

    *before_last, last = result.turns

    assert last.result.killed
    assert not any(turn.result.killed for turn in before_last)


def test_turns_are_immutable_tuple():
    hero = Character(name="Hero", max_hp=30, attack=20)

    result = fight(hero, SLIME.spawn(), rng=FakeRandom())

    assert isinstance(result.turns, tuple)


# --- Random ---


@pytest.mark.parametrize("seed", range(20))
def test_seeded_battle_always_ends_with_a_living_winner(seed):
    hero = Character(name="Hero", max_hp=30, attack=6, defense=1)
    goblin = GOBLIN.spawn()

    result = fight(hero, goblin, rng=random.Random(seed))

    winner, loser = (hero, goblin) if result.winner == "Hero" else (goblin, hero)

    assert winner.is_alive
    assert not loser.is_alive
    assert result.turns[-1].result.killed


# --- Rules ---


def test_dead_hero_cannot_fight():
    hero = Character(name="Hero", max_hp=30, hp=0, attack=5)

    with pytest.raises(ValueError, match="attacker cannot be dead"):
        fight(hero, SLIME.spawn(), rng=FakeRandom())


def test_dead_enemy_cannot_fight():
    hero = Character(name="Hero", max_hp=30, attack=5)
    slime = Character(name="Slime", max_hp=6, hp=0)

    with pytest.raises(ValueError, match="defender cannot be dead"):
        fight(hero, slime, rng=FakeRandom())


def test_cannot_fight_itself():
    hero = Character(name="Hero", max_hp=30, attack=5)

    with pytest.raises(ValueError, match="attacker cannot be the same"):
        fight(hero, hero, rng=FakeRandom())
