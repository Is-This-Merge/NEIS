from Player import Player

import pygame, random, math


class Queen(Player):
    def __init__(self, match, location):
        super().__init__(match, (200, 0, 0), location)

    def command(self):
        assigned = [s for s in self.match.soldiers if s.assignedGoal is not None]

        if len(assigned) == 0:
            return

        count = random.randint(0, min(3, len(assigned)))

        for _ in range(count):
            if not assigned:
                break
            soldier = random.choice(assigned)
            assigned.remove(soldier)
            soldier.execute_queen_command()

    def play(self):
        if self.ball.rolling or self.match.isGameOver:
            return True

        flamingo = self.getCurrentFlamingo()

        if flamingo is None or not flamingo.usable:
            self.match.isGameOver = True
            self.match.winner = self.match.players[0]
            return True

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

        angle_to_goal = math.atan2(dy, dx)
        flamingo.charge_angle = angle_to_goal + math.pi
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