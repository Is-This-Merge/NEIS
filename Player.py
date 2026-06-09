from Flamingo import Flamingo
from Hedgehog import Hedgehog

import random


class Player:
    def __init__(self, match, color, location):
        self.match = match
        self.flamingos = [Flamingo(match) for _ in range(3)]
        self.currentFlamingoIdx = 0
        self.ball = Hedgehog(self.match, color, location)
        self.passedGoals = 0

    def getCurrentFlamingo(self):
        if self.currentFlamingoIdx >= len(self.flamingos):
            return None
        return self.flamingos[self.currentFlamingoIdx]

    def has_usable_flamingo(self):
        return any(flamingo.usable for flamingo in self.flamingos)

    def replaceFlamingo(self):
        for i in range(self.currentFlamingo + 1, len(self.flamingos)):
            if self.flamingos[i].usable:
                self.currentFlamingo = i
                return True

        for i in range(0, self.currentFlamingo):
            if self.flamingos[i].usable:
                self.currentFlamingo = i
                return True

        return False

    def hit(self, strength):
        flamingo = self.get_current_flamingo()

        if flamingo is None or not flamingo.usable:
            return

        flamingo.hit(self.ball, strength)

        if strength >= 85 and random.random() < 0.01:
            self.ball.runaway()

        if not flamingo.usable:
            self.replaceFlamingo()