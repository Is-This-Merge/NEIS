import GamePlayer, Goalpost, Soldier, Post, Queen

import pygame
import random
import math


class CroquetMatch:

    def __init__(self):

        self.currentTurn = 0
        self.isWin = False

        self.width = 3500 // 4
        self.height = 2800 // 4

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption(
            "이상한 나라의 크로케 경기"
        )

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

        self.font = pygame.font.SysFont(
            "malgungothic",
            28
        )

        self.players = [
            GamePlayer(self),
            Queen(self)
        ]

        self.currentBall = self.players[0].ball

        self.post = Post()

        self.goalpostsNum = 8
        self.soldiersNum = 24

        self.goalposts = []
        self.soldiers = []

        self.current_gate = 0

        self.friction = 0.98

        self.aiming = False
        self.start_mouse = None

        self.create_map()

    def create_map(self):

        for _ in range(self.soldiersNum):

            self.soldiers.append(
                Soldier(
                    cooldown=0,
                    match=self
                )
            )

        for i in range(self.goalpostsNum):

            goalpost = Goalpost(
                location=(
                    random.randint(
                        100,
                        self.width - 100
                    ),
                    random.randint(
                        100,
                        self.height - 100
                    )
                ),
                order=i + 1
            )

            goalpost.soldiers = [
                Soldier(
                    cooldown=0,
                    assignedGoal=goalpost,
                    match=self
                )
                for _ in range(3)
            ]

            self.goalposts.append(goalpost)

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
                    self.start_mouse = (
                        pygame.mouse.get_pos()
                    )

            if (
                event.type ==
                pygame.MOUSEBUTTONUP
                and self.aiming
            ):

                end_mouse = (
                    pygame.mouse.get_pos()
                )

                dx = (
                    self.start_mouse[0]
                    - end_mouse[0]
                )

                dy = (
                    self.start_mouse[1]
                    - end_mouse[1]
                )

                power = 0.15

                self.currentBall.velocity = (
                    dx * power,
                    dy * power
                )

                self.aiming = False

        return True

    def check_gate_pass(self):

        if self.current_gate >= len(
            self.goalposts
        ):
            return

        goalpost = self.goalposts[
            self.current_gate
        ]

        gx, gy = goalpost.location

        bx, by = self.currentBall.location

        distance = math.hypot(
            bx - gx,
            by - gy
        )

        if distance < 40:
            self.current_gate += 1

    def update(self):

        bx, by = self.currentBall.location
        vx, vy = self.currentBall.velocity

        bx += vx
        by += vy

        vx *= self.friction
        vy *= self.friction

        if abs(vx) < 0.05:
            vx = 0

        if abs(vy) < 0.05:
            vy = 0

        radius = self.currentBall.radius

        if (
            bx - radius < 0
            or
            bx + radius > self.width
        ):
            vx *= -0.8

            bx = max(
                radius,
                min(
                    self.width - radius,
                    bx
                )
            )

        if (
            by - radius < 0
            or
            by + radius > self.height
        ):
            vy *= -0.8

            by = max(
                radius,
                min(
                    self.height - radius,
                    by
                )
            )

        self.currentBall.location = (
            bx,
            by
        )

        self.currentBall.velocity = (
            vx,
            vy
        )

        self.check_gate_pass()

    def draw_ball(self):

        x, y = self.currentBall.location

        pygame.draw.circle(
            self.screen,
            self.colors["PINK"],
            (int(x), int(y)),
            self.currentBall.radius
        )

        pygame.draw.circle(
            self.screen,
            self.colors["BLACK"],
            (int(x), int(y)),
            self.currentBall.radius,
            2
        )

    def draw_goalpost(
        self,
        goalpost,
        active=False
    ):

        color = (
            self.colors["YELLOW"]
            if active
            else self.colors["BLUE"]
        )

        x, y = goalpost.location

        width = 50
        height = 80

        rect = pygame.Rect(
            x - width // 2,
            y - height // 2,
            width,
            height
        )

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            3
        )

    def draw_flamingo(
        self,
        mouse_pos
    ):

        x, y = self.currentBall.location

        pygame.draw.line(
            self.screen,
            self.colors["RED"],
            (x, y),
            mouse_pos,
            5
        )

        pygame.draw.circle(
            self.screen,
            self.colors["PINK"],
            mouse_pos,
            14
        )

    def draw(self):

        self.screen.fill(
            self.colors["GREEN"]
        )

        for i in range(
            0,
            self.width,
            40
        ):

            pygame.draw.line(
                self.screen,
                self.colors["DARK_GREEN"],
                (i, 0),
                (i + 80, self.height),
                1
            )

        for i, goalpost in enumerate(
            self.goalposts
        ):

            self.draw_goalpost(
                goalpost,
                active=(
                    i ==
                    self.current_gate
                )
            )

        self.draw_ball()

        if self.aiming:

            mouse_pos = (
                pygame.mouse.get_pos()
            )

            bx, by = (
                self.currentBall.location
            )

            pygame.draw.line(
                self.screen,
                self.colors["BLACK"],
                (bx, by),
                mouse_pos,
                2
            )

            self.draw_flamingo(
                mouse_pos
            )

        if self.current_gate < len(
            self.goalposts
        ):

            text = self.font.render(
                f"현재 목표 : {self.current_gate + 1}번 문",
                True,
                self.colors["BLACK"]
            )

        else:

            text = self.font.render(
                "승리!",
                True,
                self.colors["BLACK"]
            )

        self.screen.blit(
            text,
            (20, 20)
        )

    def run(self):

        running = True

        while running:

            self.clock.tick(60)

            running = (
                self.handle_events()
            )

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()