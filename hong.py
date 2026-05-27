import * from choi
import * from kim
import * from kwak
import random

class Player():
    def __init__(self):
        self.flamingoes = [flamingo1 = Flamingo(), flamingo2 = Flamingo(), flamingo3 = Flamingo()]
        self.currentFlamingo = 0
        self.ball = Hedgehog()
        self.passedGoals = 0
    def hit(self, strength, direction):
        self.flamingoes[self.currentFlamingo].hit(strength, direction)
        if strength == 100:
            if random.random() < 0.03:
                self.ball.runaway()
    def replaceFlamingo(self):
        self.currentFlamingo += 1
