from Player import Player

import pygame

class GamePlayer(Player):
    def __init__(self, match, location):
        super().__init__(match, (150, 75, 0), location)
        # 마지막 배치 결과 (UI 표시)

    def assign_to_goal(self, goal_index):
        # 숫자키로 1명씩 배치
        if goal_index < 0 or goal_index >= len(self.match.goalposts):
            return

        if not self.match.available_soldiers:
            self.match.set_msg("배치 가능한 병사가 없습니다")
            return

        goalpost = self.match.goalposts[goal_index]
        soldier = self.match.available_soldiers[0]

        if soldier.assign(goalpost):
            self.match.set_msg(f"{goal_index + 1}번 골대에 병사 배치 완료")

    def play(self):
        flamingo = self.getCurrentFlamingo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if flamingo is None:
                self.match.isGameOver = True
                self.match.winner = self.match.players[1]
                return True

            # 숫자키로 병사 배치
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    self.assign_to_goal(event.key - pygame.K_1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.ball.rolling and not self.match.isGameOver and flamingo.usable and not flamingo.charging and not flamingo.swinging:
                    flamingo.start_charge(self.ball)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if flamingo.charging:
                    strength = flamingo.release_charge()

                    if strength is not None:
                        flamingo.hit(self.ball, strength)

                        if not flamingo.usable:
                            has_next = self.replaceFlamingo()

                            if not has_next:
                                self.match.isGameOver = True
                                self.match.winner = self.match.players[1]

        return True
