from Object import Object
import pygame, math


class Goalpost(Object):
    def __init__(self, location=(0, 0), order=1, soldiers=None, usable=True):
        super().__init__(usable)
        self.location = location
        self.order = order
        self.soldiers = soldiers if soldiers is not None else []
        # 병사가 0명이 된 시점의 턴 (없으면 None)
        self.emptySinceTurn = None

    def addSoldier(self, soldier):
        if soldier not in self.soldiers:
            self.soldiers.append(soldier)

    def has_posts(self):
        # 병사가 2명 이상이면 양쪽 기둥(골문) 형태 → 공 충돌 적용
        return len(self.soldiers) >= 2

    def draw_goalpost(self, screen):
        count = len(self.soldiers)

        if count >= 2:
            self._draw_two_posts(screen)
        elif count == 1:
            self._draw_tent(screen)
        else:
            self._draw_empty(screen)

        # 골문 번호
        x, y = self.location
        number_text = pygame.font.SysFont("malgungothic", 22).render(str(self.order), True, (0, 0, 0))
        number_rect = number_text.get_rect(center=(x, y + 55))
        screen.blit(number_text, number_rect)

    def _draw_two_posts(self, screen):
        x, y = self.location
        soldier_color = (255, 255, 255)
        line_color = (0, 0, 0)

        left_soldier_x = x - 20
        right_soldier_x = x + 20
        soldier_top_y = y - 35
        soldier_bottom_y = y + 35

        # 왼쪽 카드병정
        pygame.draw.rect(screen, soldier_color, pygame.Rect(left_soldier_x - 5, soldier_top_y, 10, 70))
        pygame.draw.circle(screen, (0, 0, 0), (left_soldier_x, soldier_top_y - 8), 7)

        # 오른쪽 카드병정
        pygame.draw.rect(screen, soldier_color, pygame.Rect(right_soldier_x - 5, soldier_top_y, 10, 70))
        pygame.draw.circle(screen, (0, 0, 0), (right_soldier_x, soldier_top_y - 8), 7)

        # 얇은 윗부분
        pygame.draw.line(screen, line_color, (left_soldier_x, soldier_top_y + 10), (right_soldier_x, soldier_top_y + 10), 2)

        # 밑동 표시
        pygame.draw.rect(screen, line_color, pygame.Rect(left_soldier_x - 7, soldier_bottom_y - 12, 14, 12), 1)
        pygame.draw.rect(screen, line_color, pygame.Rect(right_soldier_x - 7, soldier_bottom_y - 12, 14, 12), 1)

    def _draw_tent(self, screen):
        # 병사 1명: 엎드려뻗쳐로 텐트(∧) 모양을 만든 형태
        x, y = self.location
        white = (255, 255, 255)
        black = (0, 0, 0)
        skin = (255, 220, 185)

        ground_left = (x - 24, y + 30)
        ground_right = (x + 24, y + 30)
        peak = (x, y - 18)

        # 텐트(몸통) 면
        pygame.draw.polygon(screen, white, [ground_left, peak, ground_right])
        pygame.draw.polygon(screen, black, [ground_left, peak, ground_right], 2)

        # 등에 카드 무늬 한 줄
        pygame.draw.line(screen, black, (x - 8, y + 4), peak, 1)

        # 손(왼쪽 바닥)과 발(오른쪽 바닥) 표시
        pygame.draw.line(screen, black, ground_left, (ground_left[0] - 6, ground_left[1] + 6), 3)
        pygame.draw.line(screen, black, ground_right, (ground_right[0] + 6, ground_right[1] + 6), 3)

        # 머리 (왼쪽 바닥 쪽에서 숙인 모습)
        head = (ground_left[0] + 2, ground_left[1] - 8)
        pygame.draw.circle(screen, skin, head, 6)
        pygame.draw.circle(screen, black, head, 6, 1)

    def _draw_empty(self, screen):
        # 병사 0명: 무너진 빈 골대 (희미한 밑동만)
        x, y = self.location
        faded = (120, 120, 120)

        pygame.draw.rect(screen, faded, pygame.Rect(x - 27, y + 23, 14, 12), 1)
        pygame.draw.rect(screen, faded, pygame.Rect(x + 13, y + 23, 14, 12), 1)

    def draw_goal_markers(self, screen, players):
        time = pygame.time.get_ticks() / 300
        bob = math.sin(time) * 6

        for player in reversed(players):
            if player.passedGoals != self.order - 1:
                continue

            x, y = self.location

            marker_y = y - 72 + bob
            color = player.ball.color

            points = [
                (x, marker_y + 18),
                (x - 12, marker_y),
                (x + 12, marker_y)
            ]

            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (0, 0, 0), points, 2)
