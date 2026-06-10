from Object import Object
import pygame, math


class Goalpost(Object):
    def __init__(self, location, order):
        super().__init__()
        self.location = location
        self.order = order
        self.soldiers = []
        self.emptySinceTurn = None

    def addSoldier(self, soldier):
        if soldier not in self.soldiers:
            self.soldiers.append(soldier)

    def getHitBox(self):
        x, y = self.location
        count = len(self.soldiers)

        if count >= 2:
            bottom_y = y + 35
            bw, bh = 8, 8
            return [
                pygame.Rect((x - 20) - bw // 2, bottom_y - bh, bw, bh),
                pygame.Rect((x + 20) - bw // 2, bottom_y - bh, bw, bh),
            ]
        elif count == 1:
            foot_y = y + 30
            bw, bh = 7, 12
            return [
                pygame.Rect((x - 22) - bw // 2, foot_y - bh, bw, bh),
                pygame.Rect((x + 22) - bw // 2, foot_y - bh, bw, bh),
            ]
        else:
            return []

    def draw_goalpost(self, screen):
        count = len(self.soldiers)

        if count >= 2:
            x, y = self.location
            soldier_color = (255, 255, 255)
            line_color = (0, 0, 0)

            left_soldier_x = x - 20
            right_soldier_x = x + 20
            soldier_top_y = y - 35
            soldier_bottom_y = y + 35

            pygame.draw.rect(screen, soldier_color, pygame.Rect(left_soldier_x - 5, soldier_top_y, 10, 70))
            pygame.draw.circle(screen, (0, 0, 0), (left_soldier_x, soldier_top_y - 8), 7)

            pygame.draw.rect(screen, soldier_color, pygame.Rect(right_soldier_x - 5, soldier_top_y, 10, 70))
            pygame.draw.circle(screen, (0, 0, 0), (right_soldier_x, soldier_top_y - 8), 7)

            pygame.draw.line(screen, line_color, (left_soldier_x, soldier_top_y + 10), (right_soldier_x, soldier_top_y + 10), 2)
            pygame.draw.rect(screen, line_color, pygame.Rect(left_soldier_x - 7, soldier_bottom_y - 12, 14, 12), 1)
            pygame.draw.rect(screen, line_color, pygame.Rect(right_soldier_x - 7, soldier_bottom_y - 12, 14, 12), 1)
        elif count == 1:
            x, y = self.location
            black = (0, 0, 0)
            skin = (255, 220, 185)

            ground_left = (x - 26, y + 30)
            ground_right = (x + 26, y + 30)
            peak_left = (x - 9, y - 16)
            peak_right = (x + 9, y - 16)

            pygame.draw.line(screen, black, ground_left, peak_left, 4)
            pygame.draw.line(screen, black, ground_right, peak_right, 4)

            pygame.draw.line(screen, black, peak_left, peak_right, 4)

            pygame.draw.line(screen, black, ground_left, (ground_left[0] - 6, ground_left[1] + 6), 3)
            pygame.draw.line(screen, black, ground_right, (ground_right[0] + 6, ground_right[1] + 6), 3)

            head = (ground_left[0] - 2, ground_left[1] - 6)
            pygame.draw.circle(screen, skin, head, 6)
            pygame.draw.circle(screen, black, head, 6, 1)
        else:
            x, y = self.location
            faded = (120, 120, 120)
            pygame.draw.rect(screen, faded, pygame.Rect(x - 27, y + 23, 14, 12), 1)
            pygame.draw.rect(screen, faded, pygame.Rect(x + 13, y + 23, 14, 12), 1)

        #골 번호
        x, y = self.location
        number_text = pygame.font.SysFont("malgungothic", 22).render(str(self.order), True, (0, 0, 0))
        number_rect = number_text.get_rect(center=(x, y + 55))
        screen.blit(number_text, number_rect)
        

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
