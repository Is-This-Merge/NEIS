from Flamingo import Flamingo
from Hedgehog import Hedgehog


class Player:
    def __init__(self, match, color, location):
        self.match = match
        self.flamingos = [Flamingo(match) for _ in range(3)]
        self.currentFlamingoIdx = 0
        self.ball = Hedgehog(match, color, location)
        self.passedGoals = 0

    def getCurrentFlamingo(self):
        if self.currentFlamingoIdx >= len(self.flamingos):
            return None
        return self.flamingos[self.currentFlamingoIdx]

    def replaceFlamingo(self):
        # 순서대로 사용 가능한 홍학을 찾아 교체
        n = len(self.flamingos)
        for offset in range(1, n):
            i = (self.currentFlamingoIdx + offset) % n
            if self.flamingos[i].usable:
                self.currentFlamingoIdx = i
                return True
        return False
