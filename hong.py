from kim import *
from choi import *
from kwak import *
import random

class Player:
    def __init__(self, match):
        self.flamingos = [Flamingo(random.randint(30, 50), random.randint(70, 100)), Flamingo(random.randint(30, 50), random.randint(70, 100)), Flamingo(random.randint(30, 50), random.randint(70, 100))]
        self.currentFlamingo = 0
        self.ball = Hedgehog()
        self.passedGoals = 0
        self.match = match
    def hit(self, strength, direction):
        self.flamingos[self.currentFlamingo].hit(strength, direction)
        if strength >= 85:
            if random.random() < 0.005:
                self.ball.runaway()
    def replaceFlamingo(self):
        self.currentFlamingo += 1

class GamePlayer(Player):
    def __init__(self, match):
        super().__init__(match)
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
    def __init__(self, match):
        super().__init__(match)
        self.movableSoldiers = []
        self.mood = 0
        for soldier in self.match.soldiers:
            if soldier.assignedGoal is not None:
                if soldier not in self.movableSoldiers:
                    self.movableSoldiers.append(soldier)
    def hit(self, strength, direction):
        self.flamingos[self.currentFlamingo].hit(strength, direction)
    def command(self):
        for soldier in self.match.soldiers:
            if soldier.assignedGoal is not None:
                if soldier not in self.movableSoldiers:
                    self.movableSoldiers.append(soldier)
        for _ in range(random.randint(0, min(4, len(self.movableSoldiers)))):
            i = random.randrange(0, len(self.movableSoldiers))
            self.movableSoldiers[i].execute_queen_command()

class Post(object):
    def __init__(self):
        super().__init__()

