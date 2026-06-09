from Player import Player

import pygame, random, math


class Queen(Player):
    def __init__(self, match, location):
        super().__init__(match, match.colors["RED"], location)

    def command(self):
        # 현재 골대를 지키고 있는 병사들 중 일부를 빼냄
        assigned = [s for s in self.match.soldiers if s.assignedGoal is not None]

        if len(assigned) == 0:
            return

        # 한 번에 최소 0명 ~ 최대 3명까지 데려감
        count = random.randint(0, min(3, len(assigned)))

        for _ in range(count):
            if not assigned:
                break
            soldier = random.choice(assigned)
            assigned.remove(soldier)
            soldier.execute_queen_command()

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False

        if self.match.turnStarted or self.match.isGameOver:
            return True

        flamingo = self.getCurrentFlamingo()

        if flamingo is None or not flamingo.usable:
            self.match.isGameOver = True
            self.match.winner = self.match.players[0]
            return True

        # 이미 스윙 애니메이션이 진행 중이면 새로 시작하지 않음
        # (command/스윙 설정이 한 턴에 한 번만 실행되도록 보장)
        if flamingo.swinging:
            return True

        self.command()

        if self.passedGoals >= len(self.match.goalposts):
            return True

        bx, by = self.ball.location
        gx, gy = self.match.goalposts[self.passedGoals].location

        dx = gx - bx
        dy = gy - by
        length = math.hypot(dx, dy)

        if length == 0:
            return True

        power = random.uniform(8, 14)
        velocity = (dx / length * power, dy / length * power)

        # 사람 플레이어와 동일한 스윙 애니메이션 시스템을 사용
        # 홍학은 목표 반대편에 서서 공을 목표 방향으로 쳐냄
        angle_to_goal = math.atan2(dy, dx)
        flamingo.flamingo_charge_angle = angle_to_goal + math.pi
        flamingo.swing_pending_velocity = velocity
        flamingo.swing_start_time = pygame.time.get_ticks()
        flamingo.swing_hit_done = False
        flamingo.swinging = True
        flamingo.charging = False

        # 홍학을 통해 공을 쳐서 홍학 HP를 감소시킴
        flamingo.hit(self.ball, power)

        if not flamingo.usable:
            self.replaceFlamingo()

        return True