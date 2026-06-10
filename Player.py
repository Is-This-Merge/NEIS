from Flamingo import Flamingo
from Hedgehog import Hedgehog


class Player:
    def __init__(self, match, color, location):
        self.match = match
        self.__flamingos = [Flamingo(match) for _ in range(3)]
        self.currentFlamingoIdx = 0
        self.ball = Hedgehog(match, color, location)
        self.passedGoals = 0

    def getCurrentFlamingo(self):
        if self.currentFlamingoIdx >= len(self.__flamingos):
            return None
        return self.__flamingos[self.currentFlamingoIdx]

    def replaceFlamingo(self):
        self.currentFlamingoIdx += 1
        if self.currentFlamingoIdx >= len(self.__flamingos):
            return False
        return True
