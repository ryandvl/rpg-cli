from typing import TYPE_CHECKING

from src.hud.choices_bar import ChoicesBar
from src.hud.enemy_informations import EnemyInformations

if TYPE_CHECKING:
    from src.controllers.hud_controller import HudController

def create_hud_layers(h: 'HudController'):
    c = h.create_layer

    c(name='EnemyInformations', dto=EnemyInformations())
    c(name='ChoicesBar', dto=ChoicesBar())

