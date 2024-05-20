from src.controllers.game_logger import GameLogger
from src.utils.string_manipulation import equalize_string, insert_string, space_string

class ManaOptions:
    mana: int
    max_mana: int


class ManaControl:
    '''
    Control the display to player and mobs mana
    '''
    mana: float
    max_mana: float
    isPlayer: bool = False

    def __init__(self, options: ManaOptions) -> None:
        self.mana = options.mana
        self.max_mana = options.max_mana

    def getMessage(self) -> str:
        mana_size = int(
            (self.mana / self.max_mana) * 20
        )

        manaBar = insert_string(
            equalize_string(f'{self.mana}/{self.max_mana}', 20), "&reset", mana_size
        )

        return f'&reset&black[&bg_cyan' +\
            manaBar +\
            '&reset&black]&reset'

    def print(self) -> None:
        GameLogger.print(
            f'&black⊢ &bold&cyan{space_string('MANA', 10)}' +
            self.getMessage()
        )
