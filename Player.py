from Flamingo import Flamingo
from Hedgehog import Hedgehog

import random


class Player:
    def __init__(self, match, color, location):
        self.match = match
        self.flamingos = [
            Flamingo(self.match, random.randint(30, 50), random.randint(70, 100)),
            Flamingo(self.match, random.randint(30, 50), random.randint(70, 100)),
            Flamingo(self.match, random.randint(30, 50), random.randint(70, 100))
        ]
        self.currentFlamingo = 0
        self.ball = Hedgehog(self.match, random.randint(10, 20), color, location)
        self.passedGoals = 0

    def hit(self, strength, direction):
        self.flamingos[self.currentFlamingo].hit(self.ball, strength, direction)
        if strength >= 85 and random.random() < 0.01:
            self.ball.runaway()

    def replaceFlamingo(self):
        self.currentFlamingo = (self.currentFlamingo + 1) % len(self.flamingos)