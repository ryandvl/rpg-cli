import time
from typing import Any, Callable, List
from src.controllers.enemy_controller import EnemyController, EnemyOptions
from src.controllers.game_logger import GameLogger
from src.utils import terminal

function_type = Callable[..., Any]

class Action:
    aliases: List[str]
    run: function_type

    def __init__(self, aliases: List[str], run: function_type) -> None:
        self.aliases = aliases
        self.run = run


class ActionController:
    is_open: bool = False
    actions: dict[str, Action] = dict()

    def __init__(self) -> None:
        def quit_function() -> None:
            self.is_open = False
            terminal.clear()

            GameLogger.warn('Closing the game and saving your progress, please wait...')
            GameLogger.success('Progress saved!')
            
            time.sleep(1)

        self.add_action('&redQuit Game', ['q', 'qt', 'quit', 'quit game'], quit_function)

    def add_action(self, name: str, aliases: List[str], run: function_type) -> None:
        self.actions[name] = Action(aliases, run)

    def remove_action(self, name: str) -> None:
        del self.actions[name]

    def start(self) -> None:
        enemy_options = EnemyOptions()
        enemy_options.name = 'Slime'
        enemy_options.level = 7

        enemy_options.stats.max_health = 1000

        enemy = EnemyController(enemy_options)

        self.is_open = True
        while self.is_open:
            terminal.clear()

            enemy.print()

            actions = []

            for key, value in self.actions.items():
                actions.append(f'{key} &black(&yellow{value.aliases[0]}&black)')

            choice = GameLogger\
                .input(f'\n&blackSelect your action.\n{' &black| '.join(actions)}\n\n&green')\
                .lower()

            for _, value in self.actions.items():
                if choice in value.aliases:
                    value.run()
                    break
