from Object import Object
import pygame, math, random

class Hedgehog(Object):
    match = None
    def __init__(self, match, color, location):
        super().__init__()
        Hedgehog.match = match
        self.location = location
        self.radius=random.randint(10, 20)
        self.color=color
        self.velocity=(0,0)
        self.speed=0
        self.sharpness = random.randint(30, 70)

    # 도망가기
    def runaway(self):
        self.usable=False

    @classmethod
    def draw_hedgehog_ball(cls, player):
        x, y = player.ball.location
        player.ball.speed = math.hypot(*player.ball.velocity)
        r = player.ball.radius

        if player == cls.match.currentPlayer and not cls.match.isGameOver:
            time = pygame.time.get_ticks() / 250
            pulse = (math.sin(time) + 1) / 2
            highlight_radius = r + 4 + int(pulse * 6)

            pygame.draw.circle(cls.match.screen, cls.match.colors["YELLOW"], (int(x), int(y)), highlight_radius, 3)
            pygame.draw.circle(cls.match.screen, cls.match.colors["BLACK"], (int(x), int(y)), highlight_radius + 3, 1)

        if player.ball.speed < 0.2:
            # 정지 상태: 고슴도치 모양
            pygame.draw.ellipse(cls.match.screen, player.ball.color, pygame.Rect(x - r, y - r + 2, r * 2, r + 8))
            pygame.draw.circle(cls.match.screen, player.ball.color, (int(x + r * 0.65), int(y - r * 0.15)), max(4, r // 2))

            # 가시
            for i in range(4):
                sx = x - r * 0.8 + i * r * 0.28
                pygame.draw.line(
                    cls.match.screen,
                    cls.match.colors["BLACK"],
                    (int(sx), int(y - r * 0.4)),
                    (int(sx - 5), int(y - r * 0.9)),
                    2
                )

            # 눈, 코
            pygame.draw.circle(cls.match.screen, cls.match.colors["BLACK"], (int(x + r * 0.75), int(y - r * 0.3)), 2)
            pygame.draw.circle(cls.match.screen, cls.match.colors["BLACK"], (int(x + r * 1.12), int(y - r * 0.1)), 2)

            pygame.draw.ellipse(cls.match.screen, cls.match.colors["BLACK"], pygame.Rect(x - r, y - r + 2, r * 2, r + 8), 2)
        else:
            # 이동 상태: 몸을 둥글게 만 모습
            pygame.draw.circle(cls.match.screen, player.ball.color, (int(x), int(y)), r)
            pygame.draw.circle(cls.match.screen, cls.match.colors["BLACK"], (int(x), int(y)), r, 2)

            spin = pygame.time.get_ticks() / 120

            for i in range(3):
                angle = spin + i * 2.1
                sx = int(x + math.cos(angle) * r * 0.35)
                sy = int(y + math.sin(angle) * r * 0.35)
                pygame.draw.circle(cls.match.screen, cls.match.colors["BLACK"], (sx, sy), 2)