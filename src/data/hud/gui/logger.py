from typing import TYPE_CHECKING

from src.data.hud.components.choices_bar import ChoicesBar
from src.data.hud.components.enemy_informations import EnemyInformations

if TYPE_CHECKING:
    from src.controllers.hud_manager import HudManager

def create_logger_layers(h: 'HudManager'):
    c = h.create_layer

    
