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

        self.goalposts = []

    def passTurn(self):
        self.currentTurn += 1
        print(f"Turn {self.currentTurn} passed.")
    
    def playTurn(self):
        self.currentPlayer = self.players[self.currentTurn % 2]
        self.ball = self.currentPlayer.ball

        self.aiming = False
        self.start_mouse = None



class Queen(Player):
    def __init__(self):
        super().__init__()


def draw_ball(x, y):
    # 고슴도치 느낌의 공
    pygame.draw.circle(screen, PINK, (int(x), int(y)), ball_radius)
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), ball_radius, 2)

    # 가시 표현
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = x + math.cos(rad) * ball_radius
        y1 = y + math.sin(rad) * ball_radius
        x2 = x + math.cos(rad) * (ball_radius + 7)
        y2 = y + math.sin(rad) * (ball_radius + 7)
        pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2)

def draw_flamingo(mouse_pos):
    # 플라밍고 망치 느낌의 선
    pygame.draw.line(screen, RED, (ball_x, ball_y), mouse_pos, 5)
    pygame.draw.circle(screen, PINK, mouse_pos, 14)
    pygame.draw.circle(screen, BLACK, mouse_pos, 14, 2)

def draw_gate(rect, active=False):
    color = YELLOW if active else BLUE

    # 카드 병정 두 명이 서서 문을 만드는 느낌
    pygame.draw.rect(screen, color, (rect.left, rect.top, 12, rect.height))
    pygame.draw.rect(screen, color, (rect.right - 12, rect.top, 12, rect.height))
    pygame.draw.rect(screen, color, (rect.left, rect.top, rect.width, 12))

    pygame.draw.rect(screen, BLACK, rect, 2)

def check_gate_pass():
    global current_gate

    if current_gate >= len(gates):
        return

    gate = gates[current_gate]

    # 공의 중심이 현재 골대 사각형 안에 들어가면 통과 처리
    if gate.collidepoint(ball_x, ball_y):
        current_gate += 1

running = True

while running:
    clock.tick(60)
    screen.fill(GREEN)

    # 배경 잔디
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, DARK_GREEN, (i, 0), (i + 80, HEIGHT), 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 마우스를 누르면 조준 시작
        if event.type == pygame.MOUSEBUTTONDOWN:
            speed = math.hypot(ball_vx, ball_vy)
            if speed < 0.5:
                aiming = True
                start_mouse = pygame.mouse.get_pos()

        # 마우스를 떼면 공 치기
        if event.type == pygame.MOUSEBUTTONUP and aiming:
            end_mouse = pygame.mouse.get_pos()

            dx = start_mouse[0] - end_mouse[0]
            dy = start_mouse[1] - end_mouse[1]

            power = 0.15
            ball_vx = dx * power
            ball_vy = dy * power

            aiming = False

    # 공 이동
    ball_x += ball_vx
    ball_y += ball_vy

    # 마찰 적용
    ball_vx *= FRICTION
    ball_vy *= FRICTION

    # 너무 느리면 정지
    if abs(ball_vx) < 0.05:
        ball_vx = 0
    if abs(ball_vy) < 0.05:
        ball_vy = 0

    # 벽 충돌
    if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
        ball_vx *= -0.8
        ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))

    if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
        ball_vy *= -0.8
        ball_y = max(ball_radius, min(HEIGHT - ball_radius, ball_y))

    check_gate_pass()

    # 골대 그리기
    for i, gate in enumerate(gates):
        draw_gate(gate, active=(i == current_gate))

    # 공 그리기
    draw_ball(ball_x, ball_y)

    # 조준선
    if aiming:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, BLACK, (ball_x, ball_y), mouse_pos, 2)
        draw_flamingo(mouse_pos)

    # UI
    if current_gate < len(gates):
        text = font.render(f"현재 목표: {current_gate + 1}번 카드 병정 문 통과", True, BLACK)
    else:
        text = font.render("승리! 모든 문을 통과했습니다!", True, BLACK)

    screen.blit(text, (20, 20))

    guide = font.render("마우스를 드래그해서 고슴도치를 치세요", True, BLACK)
    screen.blit(guide, (20, 55))

    pygame.display.flip()

pygame.quit()