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
        self.goals = []
        self.terrain = []
        self.players = [GamePlayer(self), Queen(self)]
        self.currentBall = self.players[0].ball
        self.friction = 0.98
        self.aiming = False
        self.start_mouse = None

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

        self.goalpostsNum = 8
        self.soldiersNum = 24

        self.soldiers = []
        for i in range(self.soldiersNum):
            self.soldiers.append(Soldier(cooldown=0, match=self))

        self.goalposts = []
        for i in range(self.goalpostsNum):
            self.goalposts.append(Goalpost(location=(random.randint(100, self.width-100), random.randint(100, self.height-100)), order=i+1))
            self.goalposts[i].soldiers = [Soldier(cooldown=0, assignedGoal=self.goalposts[i], match=self) for _ in range(3)]

        


    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:

                speed = math.hypot(
                    self.currentBall.velocity[0],
                    self.currentBall.velocity[1]
                )

                if speed < 0.5:
                    self.aiming = True
                    self.start_mouse = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP and self.aiming:

                end_mouse = pygame.mouse.get_pos()

                dx = self.start_mouse[0] - end_mouse[0]
                dy = self.start_mouse[1] - end_mouse[1]

                power = 0.15

                self.currentBall.velocity = (dx * power, dy * power)

                self.aiming = False

        return True
    
    def check_gate_pass(self):

        if self.current_gate >= len(self.gates):
            return

        gate = self.gates[self.current_gate]

        if gate.collidepoint(
            self.currentBall.location[0],
            self.currentBall.location[1]
        ):
            self.current_gate += 1

    def update(self):
        self.currentBall.location = (
            self.currentBall.location[0] + self.currentBall.velocity[0],
            self.currentBall.location[1] + self.currentBall.velocity[1]
        )

        self.ball_vx *= self.friction
        self.ball_vy *= self.friction

        if abs(self.ball_vx) < 0.05:
            self.ball_vx = 0

        if abs(self.ball_vy) < 0.05:
            self.ball_vy = 0

        # 벽 충돌
        if (
            self.currentBall.location[0] - self.currentBall.radius < 0 or
            self.currentBall.location[0] + self.currentBall.radius > self.width
        ):
            self.currentBall.velocity = (-self.currentBall.velocity[0] * 0.8, self.currentBall.velocity[1])

            self.currentBall.location = (
                max(
                    self.currentBall.radius,
                    min(
                        self.width - self.currentBall.radius,
                        self.currentBall.location[0]
                    )
                ),
                self.currentBall.location[1]
            )

        if (
            self.currentBall.location[1] - self.currentBall.radius < 0 or
            self.currentBall.location[1] + self.currentBall.radius > self.height
        ):
            self.currentBall.velocity = (self.currentBall.velocity[0], -self.currentBall.velocity[1])

            self.currentBall.location = (
                self.currentBall.location[0],
                max(
                    self.currentBall.radius,
                    min(
                        self.height - self.currentBall.radius,
                        self.currentBall.location[1]
                    )
                )
                )
            )

        self.check_gate_pass()

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

pygame.quit()