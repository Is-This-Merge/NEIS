from choi import * 
from kim import * 
from kwak import * 
import random

class Player:
    def __init__(self):
        self.flamingoes = [Flamingo(), Flamingo(), Flamingo()]
        self.currentFlamingo = 0
        self.ball = Hedgehog()
        self.passedGoals = 0
    def hit(self, strength, direction):
        self.flamingoes[self.currentFlamingo].hit(strength, direction)
        if strength == 100:
            if random.random() < 0.005:
                self.ball.runaway()
    def replaceFlamingo(self):
        self.currentFlamingo += 1

class GamePlayer(Player):
    def __init__(self):
        super().__init__()
        self.availableSoldiers = []
    def soldierArrange(self):
        if self.availableSoldiers == []:
            print("배치 가능한 병사가 없습니다.")
        else:
            print("배치 가능한 병사 리스트:\n", self.availableSoldiers)
            curSoldier = int(input("병사의 index를 입력하세요(1부터 시작): "))
            toGoal = int(input("목적지 골대번호를 입력하세요: "))
            self.availableSoldiers[curSoldier].move(toGoal)

class Queen(Player):
    def __init__(self):
        super().__init__()
        self.movableSoldiers = []
        self.mood = 0

    def command(self):
        pass

class Post(object):
    def __init__(self):
        super().__init__()

