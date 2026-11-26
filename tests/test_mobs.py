from dataclasses import FrozenInstanceError

import pytest

from rpg_cli.domain.mobs import GOBLIN, SLIME, WOLF, MobTemplate

ALL_MOBS = [SLIME, GOBLIN, WOLF]

# --- Spawn ---


@pytest.mark.parametrize("template", ALL_MOBS, ids=lambda t: t.name)
def test_spawn_copies_template_stats(template: MobTemplate):
    mob = template.spawn()

    assert mob.name == template.name
    assert mob.max_hp == template.max_hp
    assert mob.attack == template.attack
    assert mob.defense == template.defense
    assert mob.crit_chance == template.crit_chance


@pytest.mark.parametrize("template", ALL_MOBS, ids=lambda t: t.name)
def test_spawn_starts_with_full_hp(template: MobTemplate):
    mob = template.spawn()

    assert mob.hp == template.max_hp


def test_spawn_returns_independent_instances():
    goblin_a = GOBLIN.spawn()
    goblin_b = GOBLIN.spawn()

    assert goblin_a is not goblin_b

    goblin_a.take_damage(5)

    assert goblin_a.hp == GOBLIN.max_hp - 5
    assert goblin_b.hp == GOBLIN.max_hp


# --- Template ---


def test_template_is_immutable():
    with pytest.raises(FrozenInstanceError):
        GOBLIN.max_hp = 999  # type: ignore[misc]


def test_damaging_a_spawn_does_not_change_template():
    goblin = GOBLIN.spawn()

    goblin.take_damage(5)

    assert GOBLIN.max_hp == 12
