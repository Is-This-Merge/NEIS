from Player import Player

import random

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