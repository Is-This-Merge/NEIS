from Object import Object
import pygame, math

class Goalpost(Object):
    def __init__(self, location=(0, 0), order=1, soldiers=None, usable=True):
        super().__init__(usable)
        self.location = location
        self.order = order
        self.soldiers = soldiers if soldiers is not None else []

    def addSoldier(self, soldier):
        if soldier not in self.soldiers:
            self.soldiers.append(soldier)

    def draw_goalpost(self, screen):
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

        # 골문 번호
        number_text = pygame.font.SysFont("malgungothic", 22).render(str(self.order), True, (0, 0, 0))
        number_rect = number_text.get_rect(center=(x, y + 55))
        screen.blit(number_text, number_rect)

    def draw_goal_markers(self, screen, players):
        time = pygame.time.get_ticks() / 300
        bob = math.sin(time) * 6

        for player in players:
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