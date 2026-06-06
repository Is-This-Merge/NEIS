from Player import Player

import pygame, math


class GamePlayer(Player):
    def __init__(self, match, location):
        super().__init__(match, match.colors["BROWN"], location)
        self.availableSoldiers = []

        for soldier in self.match.soldiers:
            if soldier.assignedGoal is None:
                self.availableSoldiers.append(soldier)

    def soldierArrange(self):
        for soldier in self.match.soldiers:
            if soldier.assignedGoal is None and soldier not in self.availableSoldiers:
                self.availableSoldiers.append(soldier)

        if self.availableSoldiers == []:
            print("배치 가능한 병사가 없습니다.")
            return

        print("배치 가능한 병사 리스트:\n", self.availableSoldiers)
        curSoldier = int(input("병사의 index를 입력하세요(1부터 시작): "))
        goalNum = int(input("목적지 골대번호를 입력하세요: "))
        self.availableSoldiers[curSoldier - 1].move(goalNum)

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                speed = math.hypot(*self.ball.velocity)

                if speed < 0.5 and not self.match.isGameOver and not self.match.swinging:
                    self.match.charging = True
                    self.match.mouse_down_time = pygame.time.get_ticks()

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    bx, by = self.ball.location
                    self.match.flamingo_charge_angle = math.atan2(mouse_y - by, mouse_x - bx)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.match.charging:
                angle = self.match.flamingo_charge_angle

                hold_time = pygame.time.get_ticks() - self.match.mouse_down_time
                hold_ratio = min(hold_time / self.match.max_hold_time, 1)
                power = self.match.min_power + (self.match.max_power - self.match.min_power) * hold_ratio

                self.match.swing_pending_velocity = (math.cos(angle) * power, math.sin(angle) * power)
                self.match.swing_base_angle = angle
                self.match.swing_start_time = pygame.time.get_ticks()
                self.match.swing_hit_done = False
                self.match.swinging = True
                self.match.charging = False

                self.flamingos[self.currentFlamingo].hit(self.ball, power)
                if self.flamingos[self.currentFlamingo].usable == False:
                    if self.currentFlamingo == len(self.flamingos) - 1:
                        self.match.isGameOver = True
                        self.match.winner = self.match.currentTurn % 2
                    self.currentFlamingo += 1

        return True