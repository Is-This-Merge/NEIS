from Player import Player

import pygame, random, math


class Queen(Player):
    def __init__(self, match, location):
        super().__init__(match, match.colors["RED"], location)
        self.movableSoldiers = []
        self.mood = 0

        for soldier in self.match.soldiers:
            if soldier.assignedGoal is not None:
                self.movableSoldiers.append(soldier)

    def command(self):
        for soldier in self.match.soldiers:
            if soldier.assignedGoal is not None and soldier not in self.movableSoldiers:
                self.movableSoldiers.append(soldier)

        if len(self.movableSoldiers) == 0:
            return

        for _ in range(random.randint(0, min(4, len(self.movableSoldiers)))):
            i = random.randrange(0, len(self.movableSoldiers))
            self.movableSoldiers[i].execute_queen_command()

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False

        if self.match.turnStarted or self.match.isWin:
            return True

        self.command()

        if self.passedGoals >= len(self.match.goalposts):
            return True

        bx, by = self.ball.location
        gx, gy = self.match.goalposts[self.passedGoals].location

        dx = gx - bx
        dy = gy - by
        length = math.hypot(dx, dy)

        if length == 0:
            return True

        power = random.uniform(8, 14)
        self.ball.velocity = (dx / length * power, dy / length * power)
        self.match.turnStarted = True

        return True