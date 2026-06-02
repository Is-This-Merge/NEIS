from hong import *
from kim import * 
from kwak import * 
import random
import pygame
import math

class CroquetMatch:
    def __init__(self):
        self.currentTurn = 0
        self.isWin = False
        self.soldiers = []
        self.goals = []
        self.terrain = []
        self.players = [GamePlayer(), Queen()]
        self.currentBall = self.players[0].ball
        self.friction = 0.98
        self.aiming = False

        self.width, self.height = 3500/4, 2800/4
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("이상한 나라의 크로케 경기")
        self.clock = pygame.time.Clock()
        self.colors = {
            "GREEN": (34, 177, 76),
            "DARK_GREEN": (0, 100, 0),
            "PINK": (255, 105, 180),
            "RED": (200, 0, 0),
            "YELLOW": (255, 255, 0),
            "BLUE": (0, 0, 255),
            "BLACK": (0, 0, 0)
        }
        self.font = pygame.font.SysFont("malgungothic", 28)

        self.post = Post()

        self.goalposts = []
        for i in range(8):
            self.goalposts.append(Goalpost(location=(random.randint(100, self.width-100), random.randint(100, self.height-100)), order=i+1))
            self.goalposts[i].soldiers = [Soldier(cooldown=random.randint(5, 15), assignedGoal=self.goalposts[i]) for _ in range(3)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            if not self.handle_events():
                break
            self.update()
            self.draw()
            pygame.display.flip()

class Queen(Player):
    def __init__(self):
        super().__init__()

pygame.quit()