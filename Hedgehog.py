import pygame, math, random

class Hedgehog():
    match = None
    def __init__(self, match, color, location):
        super().__init__()
        Hedgehog.match = match
        self.location = location
        self.radius=random.randint(8, 15)
        self.color=color
        self.velocity=(0,0)
        self.speed = 0
        self.sharpness = random.randint(30, 70)
        self.roundness = 0.95
        self.rolling = False

    def roll(self):
        bx, by = self.location
        vx, vy = self.velocity
        bx += vx
        by += vy
        if(vx and vy and 0 <= int(bx) < Hedgehog.match.height and 0 <= int(by) < Hedgehog.match.width):
            vx += Hedgehog.match.ground[int(bx)][int(by)][0] / 100
            vy += Hedgehog.match.ground[int(bx)][int(by)][1] / 100
        vx *= self.roundness
        vy *= self.roundness
        if abs(vx) < 0.05:
            vx = 0
        if abs(vy) < 0.05:
            vy = 0

        # 경기장 경계 문제 해결
        left_bound = 0
        right_bound = Hedgehog.match.width
        top_bound = Hedgehog.match.ui_height
        bottom_bound = Hedgehog.match.height

        if bx - self.radius < left_bound or bx + self.radius > right_bound:
            vx *= -0.8
            bx = max(left_bound + self.radius, min(right_bound - self.radius, bx))
        
        if by - self.radius < top_bound or by + self.radius > bottom_bound:
            vy *= -0.8
            by = max(top_bound + self.radius, min(bottom_bound - self.radius, by))

        for goalpost in Hedgehog.match.goalposts:
            for hb in goalpost.hitBox():
                if pygame.Rect(bx-self.radius, by-self.radius, self.radius*2, self.radius*2).colliderect(hb):
                    if bx < hb.centerx:
                        vx = -abs(vx) * 0.75
                        bx = hb.left - self.radius
                    else:
                        vx = abs(vx) * 0.75
                        bx = hb.right + self.radius
                    vy *= 0.85
                    break

        self.location = bx, by
        self.velocity = vx, vy
        self.speed = math.hypot(*self.velocity) 


    def draw_ball(self, now):
        x, y = self.location
        self.speed = math.hypot(*self.velocity)
        r = self.radius

        if now:
            time = pygame.time.get_ticks() / 250
            pulse = (math.sin(time) + 1) / 2
            highlight_radius = r + 4 + int(pulse * 6)

            pygame.draw.circle(Hedgehog.match.screen, (255, 255, 0), (int(x), int(y)), highlight_radius, 3)
            pygame.draw.circle(Hedgehog.match.screen, (0, 0, 0), (int(x), int(y)), highlight_radius + 3, 1)

        if self.speed < 0.2:
            # 정지 상태 몸
            pygame.draw.ellipse(Hedgehog.match.screen, self.color, pygame.Rect(x - r, y - r + 2, r * 2, r + 8))
            pygame.draw.circle(Hedgehog.match.screen, self.color, (int(x + r * 0.65), int(y - r * 0.15)), max(4, r // 2))

            # 가시
            for i in range(4):
                sx = x - r * 0.8 + i * r * 0.28
                pygame.draw.line(Hedgehog.match.screen, (0, 0, 0), (int(sx), int(y - r * 0.4)), (int(sx - 5), int(y - r * 0.9)), 2)

            # 눈, 코
            pygame.draw.circle(Hedgehog.match.screen, (0, 0, 0), (int(x + r * 0.75), int(y - r * 0.3)), 2)
            pygame.draw.circle(Hedgehog.match.screen, (0, 0, 0), (int(x + r * 1.12), int(y - r * 0.1)), 2)
            pygame.draw.ellipse(Hedgehog.match.screen, (0, 0, 0), pygame.Rect(x - r, y - r + 2, r * 2, r + 8), 2)
        else:
            # 이동 상태
            pygame.draw.circle(Hedgehog.match.screen, self.color, (int(x), int(y)), r)
            pygame.draw.circle(Hedgehog.match.screen, (0, 0, 0), (int(x), int(y)), r, 2)
            spin = pygame.time.get_ticks() / 120
            for i in range(3):
                angle = spin + i * 2.1
                sx = int(x + math.cos(angle) * r * 0.35)
                sy = int(y + math.sin(angle) * r * 0.35)
                pygame.draw.circle(Hedgehog.match.screen, (0, 0, 0), (sx, sy), 2)