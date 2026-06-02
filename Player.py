from Flamingo import Flamingo
from Hedgehog import Hedgehog

import random

class Player:
    def __init__(self, match):
        self.flamingos = [Flamingo(random.randint(30, 50), random.randint(70, 100)), Flamingo(random.randint(30, 50), random.randint(70, 100)), Flamingo(random.randint(30, 50), random.randint(70, 100))]
        self.currentFlamingo = 0
        self.ball = Hedgehog(random.randint(10, 20), "brown", (0, 0))
        self.passedGoals = 0
        self.match = match
    def hit(self, strength, direction):
        self.flamingos[self.currentFlamingo].hit(strength, direction)
        if strength >= 85:
            if random.random() < 0.005:
                self.ball.runaway()
    def replaceFlamingo(self):
        self.currentFlamingo += 1