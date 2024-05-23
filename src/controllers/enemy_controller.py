from src.controllers.game_logger import GameLogger
from src.controllers.stats.stats_control import StatsControl, StatsOptions

class EnemyOptions:
    name: str
    level: int = 0

    stats: StatsOptions = StatsOptions()

class EnemyController:
    name: str
    level: int

    stats: StatsControl

    def __init__(self, options: EnemyOptions) -> None:
        self.name = options.name
        self.level = options.level

        self.stats = StatsControl(options.stats)
        pass

    def attack(self):
        pass

    def print(self):
        GameLogger.print(\
            f'&bold&red⚔ {self.name} &reset&black[Lvl. &bold&white{self.level:02d}&reset&black]\n'
        )

        self.stats.print_all()
