class FakeRandom:
    def __init__(self, variance: float = 1.0, roll: float = 0.99) -> None:
        self.variance = variance
        self.roll = roll

    def uniform(self, a: float, b: float) -> float:
        return self.variance

    def random(self) -> float:
        return self.roll
