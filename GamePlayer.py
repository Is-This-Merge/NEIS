from Player import Player

import pygame
import math


class GamePlayer(Player):
    def __init__(self, match, location):
        super().__init__(match, match.colors["BROWN"], location)
        # 마지막 배치 결과 메시지 (UI 피드백용)
        self.last_assign_msg = ""
        self.last_assign_time = 0

    def available_soldiers(self):
        # 현재 배치 가능한(쿨다운이 지난 미배치) 병사 목록
        return [s for s in self.match.soldiers if s.is_available(self.match.currentTurn)]

    def assign_to_goal(self, goal_index):
        # 숫자키로 호출: available 병사 1명을 goal_index 골대에 배치
        if goal_index < 0 or goal_index >= len(self.match.goalposts):
            return

        available = self.available_soldiers()

        if not available:
            self._set_msg("배치 가능한 병사가 없습니다")
            return

        goalpost = self.match.goalposts[goal_index]
        soldier = available[0]

        if soldier.assign(goalpost):
            self._set_msg(f"{goal_index + 1}번 골대에 병사 배치 완료")

    def _set_msg(self, msg):
        self.last_assign_msg = msg
        self.last_assign_time = pygame.time.get_ticks()

    def play(self):
        flamingo = self.get_current_flamingo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if flamingo is None:
                self.match.isGameOver = True
                self.match.winner = self.match.players[1]
                return True

            # 숫자키 1~8: 해당 골대에 available 병사 배치
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    self.assign_to_goal(event.key - pygame.K_1)

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
