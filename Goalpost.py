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

    def collision_rects(self):
        # 골대 형태(병사 수)에 따른 공 충돌 히트박스 목록
        x, y = self.location
        count = len(self.soldiers)

        if count >= 2:
            # 양쪽 기둥의 밑동 (작은 히트박스)
            bottom_y = y + 35
            bw, bh = 8, 8
            return [
                pygame.Rect((x - 20) - bw // 2, bottom_y - bh, bw, bh),
                pygame.Rect((x + 20) - bw // 2, bottom_y - bh, bw, bh),
            ]
        elif count == 1:
            # 텐트의 양다리(발) — 가운데 간격은 비워 공이 통과 가능하게 함
            foot_y = y + 30
            bw, bh = 7, 12
            return [
                pygame.Rect((x - 22) - bw // 2, foot_y - bh, bw, bh),
                pygame.Rect((x + 22) - bw // 2, foot_y - bh, bw, bh),
            ]
        else:
            # 빈 골대: 충돌 없음
            return []

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
        # 병사 1명: 엎드려뻗쳐로 가운데가 뚫린 아치(∩) 텐트를 만든 형태
        # 공이 다리 사이(가운데)로 통과할 수 있음
        x, y = self.location
        black = (0, 0, 0)
        skin = (255, 220, 185)

        ground_left = (x - 26, y + 30)
        ground_right = (x + 26, y + 30)
        peak_left = (x - 9, y - 16)
        peak_right = (x + 9, y - 16)

        # 아치 다리 (양옆) — 가운데는 비워서 공이 지나갈 수 있게 함
        pygame.draw.line(screen, black, ground_left, peak_left, 4)
        pygame.draw.line(screen, black, ground_right, peak_right, 4)

        # 등(아치 윗부분) — 살짝 굽은 모양
        pygame.draw.line(screen, black, peak_left, peak_right, 4)

        # 손(왼쪽 바닥)과 발(오른쪽 바닥) 표시
        pygame.draw.line(screen, black, ground_left, (ground_left[0] - 6, ground_left[1] + 6), 3)
        pygame.draw.line(screen, black, ground_right, (ground_right[0] + 6, ground_right[1] + 6), 3)

        # 머리 (왼쪽 바닥 쪽에서 숙인 모습)
        head = (ground_left[0] - 2, ground_left[1] - 6)
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
