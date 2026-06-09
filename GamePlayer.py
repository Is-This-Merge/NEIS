from Player import Player

import pygame
import math


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
        flamingo = self.get_current_flamingo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if flamingo is None:
                self.match.isGameOver = True
                self.match.winner = self.match.players[1]
                return True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                speed = math.hypot(*self.ball.velocity)

                if speed < 0.5 and not self.match.isGameOver and flamingo.usable and not flamingo.charging and not flamingo.swinging:
                    flamingo.start_charge(self.ball)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if flamingo.charging:
                    strength = flamingo.release_charge(self.ball)

                    if strength is not None:
                        flamingo.hit(self.ball, strength)

                        if not flamingo.usable:
                            has_next = self.replaceFlamingo()

                            if not has_next:
                                self.match.isGameOver = True
                                self.match.winner = self.match.players[1]

        return True