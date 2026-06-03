from GamePlayer import GamePlayer
from Goalpost import Goalpost
from Soldier import Soldier
from Post import Post
from Queen import Queen

import pygame, random, math


class CroquetMatch:
    def __init__(self):
        self.currentTurn = 0
        self.turnStarted = False
        self.isWin = False
        self.winner = None
        self.width, self.height = 3500 // 4, 2800 // 4

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("이상한 나라의 크로케 경기")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("malgungothic", 28)

        self.colors = {
            "GREEN": (34, 177, 76),
            "DARK_GREEN": (0, 100, 0),
            "PINK": (255, 105, 180),
            "RED": (200, 0, 0),
            "YELLOW": (255, 255, 0),
            "BLUE": (0, 0, 255),
            "BLACK": (0, 0, 0),
            "BROWN": (150, 75, 0),
            "WHITE": (255, 255, 255),
            "ORANGE": (255, 165, 0)
        }

        self.post = Post()
        self.goalpostsNum = 8
        self.soldiersNum = 24
        self.goalposts = []
        self.soldiers = []

        self.friction = 0.975
        self.aiming = False
        self.start_mouse = None

        # 홍학 채 조작 관련 상태
        self.charging = False
        self.swinging = False
        self.mouse_down_time = 0
        self.max_hold_time = 2000
        self.min_power = 2.5
        self.max_power = 12

        # 홍학 스윙 애니메이션 상태
        self.swing_start_time = 0
        self.swing_duration = 300
        self.swing_hit_done = False
        self.swing_pending_velocity = (0, 0)
        self.swing_base_angle = 0
        self.flamingo_charge_angle = 0

        self.soldiers = [Soldier(cooldown=0, match=self) for _ in range(self.soldiersNum)]

        # 골문끼리 겹치지 않게 배치
        min_goalpost_distance = 130

        for i in range(self.goalpostsNum):
            while True:
                location = (random.randint(100, self.width - 100), random.randint(100, self.height - 100))
                is_overlap = False

                for other_goalpost in self.goalposts:
                    ox, oy = other_goalpost.location
                    distance = math.hypot(location[0] - ox, location[1] - oy)

                    if distance < min_goalpost_distance:
                        is_overlap = True
                        break

                if not is_overlap:
                    break

            goalpost = Goalpost(location=location, order=i + 1)
            goalpost.soldiers = [Soldier(cooldown=0, assignedGoal=goalpost, match=self) for _ in range(3)]
            self.goalposts.append(goalpost)

        self.center = (self.width // 2, self.height // 2)

        self.players = [
            GamePlayer(self, (self.center[0] - 40, self.center[1])),
            Queen(self, (self.center[0] + 40, self.center[1]))
        ]

        # 공 크기 조금 줄이기
        for player in self.players:
            player.ball.radius = max(8, int(player.ball.radius * 0.75))

        self.currentPlayer = self.players[0]
        self.currentBall = self.currentPlayer.ball

    def update(self):
        if self.isWin: return

        # 홍학 스윙 애니메이션 처리
        if self.swinging:
            elapsed = pygame.time.get_ticks() - self.swing_start_time
            progress = min(elapsed / self.swing_duration, 1)

            if progress >= 0.55 and not self.swing_hit_done:
                self.currentBall.velocity = self.swing_pending_velocity
                self.turnStarted = True
                self.swing_hit_done = True

            if progress >= 1:
                self.swinging = False

        bx, by = self.currentBall.location
        vx, vy = self.currentBall.velocity

        bx -= vx
        by -= vy
        vx *= self.friction
        vy *= self.friction

        if abs(vx) < 0.05: vx = 0
        if abs(vy) < 0.05: vy = 0

        radius = self.currentBall.radius

        # 화면 경계 튕김
        if bx - radius < 0 or bx + radius > self.width:
            vx *= -0.8
            bx = max(radius, min(self.width - radius, bx))

        if by - radius < 0 or by + radius > self.height:
            vy *= -0.8
            by = max(radius, min(self.height - radius, by))

        # 골대 충돌 판정: 카드병정의 밑동 부분에만 적용
        for goalpost in self.goalposts:
            gx, gy = goalpost.location

            left_x = gx - 20
            right_x = gx + 20
            top_y = gy - 35
            bottom_y = gy + 35

            base_width = 14
            base_height = 12

            left_base = pygame.Rect(left_x - base_width // 2, bottom_y - base_height, base_width, base_height)
            right_base = pygame.Rect(right_x - base_width // 2, bottom_y - base_height, base_width, base_height)
            ball_rect = pygame.Rect(bx - radius, by - radius, radius * 2, radius * 2)

            if ball_rect.colliderect(left_base):
                vx = -abs(vx) * 0.75 if bx < left_base.centerx else abs(vx) * 0.75
                vy *= 0.85
                bx = left_base.left - radius if bx < left_base.centerx else left_base.right + radius

            elif ball_rect.colliderect(right_base):
                vx = -abs(vx) * 0.75 if bx < right_base.centerx else abs(vx) * 0.75
                vy *= 0.85
                bx = right_base.left - radius if bx < right_base.centerx else right_base.right + radius

        self.currentBall.location = (bx, by)
        self.currentBall.velocity = (vx, vy)

        # 현재 플레이어의 목표 골문 통과 체크
        if self.currentPlayer.passedGoals >= len(self.goalposts):
            self.isWin = True
            self.winner = self.currentPlayer
            return

        goalpost = self.goalposts[self.currentPlayer.passedGoals]
        gx, gy = goalpost.location
        distance = math.hypot(bx - gx, by - gy)

        if distance < 32:
            self.currentPlayer.passedGoals += 1

            if self.currentPlayer.passedGoals >= len(self.goalposts):
                self.isWin = True
                self.winner = self.currentPlayer

        # 공이 멈추면 턴 넘기기
        self.currentBall.speed = math.hypot(*self.currentBall.velocity)

        if self.turnStarted and self.currentBall.speed < 0.1:
            self.currentBall.velocity = (0, 0)
            self.turnStarted = False
            self.aiming = False
            self.charging = False
            self.swinging = False
            self.currentTurn += 1

    def draw(self):
        def draw_hedgehog_ball(player):
            x, y = player.ball.location
            player.ball.speed = math.hypot(*player.ball.velocity)
            r = player.ball.radius

            # 현재 선택된 공 강조 표시: 시간에 따라 커졌다 작아짐
            if player == self.currentPlayer and not self.isWin:
                time = pygame.time.get_ticks() / 250
                pulse = (math.sin(time) + 1) / 2
                highlight_radius = r + 4 + int(pulse * 6)

                pygame.draw.circle(self.screen, self.colors["YELLOW"], (int(x), int(y)), highlight_radius, 3)
                pygame.draw.circle(self.screen, self.colors["BLACK"], (int(x), int(y)), highlight_radius + 3, 1)

            if player.ball.speed < 0.2:
                # 정지 상태: 고슴도치 모양
                pygame.draw.ellipse(self.screen, player.ball.color, pygame.Rect(x - r, y - r + 2, r * 2, r + 8))
                pygame.draw.circle(self.screen, player.ball.color, (int(x + r * 0.65), int(y - r * 0.15)), max(4, r // 2))

                # 가시
                for i in range(-3, 4):
                    sx = x - r * 0.8 + i * r * 0.28
                    pygame.draw.line(
                        self.screen,
                        self.colors["BLACK"],
                        (int(sx), int(y - r * 0.4)),
                        (int(sx - 5), int(y - r * 0.9)),
                        2
                    )

                # 눈, 코
                pygame.draw.circle(self.screen, self.colors["BLACK"], (int(x + r * 0.75), int(y - r * 0.3)), 2)
                pygame.draw.circle(self.screen, self.colors["BLACK"], (int(x + r * 1.12), int(y - r * 0.1)), 2)

                # 테두리
                pygame.draw.ellipse(self.screen, self.colors["BLACK"], pygame.Rect(x - r, y - r + 2, r * 2, r + 8), 2)
            else:
                # 이동 상태: 몸을 둥글게 만 모습
                pygame.draw.circle(self.screen, player.ball.color, (int(x), int(y)), r)
                pygame.draw.circle(self.screen, self.colors["BLACK"], (int(x), int(y)), r, 2)

                # 굴러가는 느낌의 곡선
                spin = pygame.time.get_ticks() / 120
                for i in range(3):
                    angle = spin + i * 2.1
                    sx = int(x + math.cos(angle) * r * 0.35)
                    sy = int(y + math.sin(angle) * r * 0.35)
                    pygame.draw.circle(self.screen, self.colors["BLACK"], (sx, sy), 2)

        def draw_goalpost(goalpost, active=False):
            x, y = goalpost.location
            soldier_color = self.colors["WHITE"]
            line_color = self.colors["BLACK"]

            left_soldier_x = x - 20
            right_soldier_x = x + 20
            soldier_top_y = y - 35
            soldier_bottom_y = y + 35

            # 현재 넣어야 하는 골대 위에 삼각형 표시
            if active:
                pygame.draw.polygon(
                    self.screen,
                    self.colors["BLACK"],
                    [(x, y - 65), (x - 10, y - 48), (x + 10, y - 48)]
                )

            # 왼쪽 카드병정
            pygame.draw.rect(self.screen, soldier_color, pygame.Rect(left_soldier_x - 5, soldier_top_y, 10, 70))
            pygame.draw.circle(self.screen, self.colors["BLACK"], (left_soldier_x, soldier_top_y - 8), 7)

            # 오른쪽 카드병정
            pygame.draw.rect(self.screen, soldier_color, pygame.Rect(right_soldier_x - 5, soldier_top_y, 10, 70))
            pygame.draw.circle(self.screen, self.colors["BLACK"], (right_soldier_x, soldier_top_y - 8), 7)

            # 얇은 윗부분
            pygame.draw.line(self.screen, line_color, (left_soldier_x, soldier_top_y + 10), (right_soldier_x, soldier_top_y + 10), 2)

            # 밑동 표시
            pygame.draw.rect(self.screen, line_color, pygame.Rect(left_soldier_x - 7, soldier_bottom_y - 12, 14, 12), 1)
            pygame.draw.rect(self.screen, line_color, pygame.Rect(right_soldier_x - 7, soldier_bottom_y - 12, 14, 12), 1)

            # 골문 번호
            number_text = self.font.render(str(goalpost.order), True, self.colors["BLACK"])
            number_rect = number_text.get_rect(center=(x, y + 55))
            self.screen.blit(number_text, number_rect)

        def draw_flamingo_handle():
            bx, by = self.currentBall.location
            mx, my = pygame.mouse.get_pos()

            dx = mx - bx
            dy = my - by
            length = math.hypot(dx, dy)

            if length == 0:
                dx, dy = 1, 0
                length = 1

            # 공 -> 마우스 방향
            aim_angle = math.atan2(dy, dx)

            # 차징/스윙 중에는 누른 순간의 방향을 유지
            if self.charging or self.swinging:
                aim_angle = self.flamingo_charge_angle

            # 홍학은 공-마우스 선에 수직으로 서 있음
            stand_angle = aim_angle + math.pi / 2

            ux, uy = math.cos(stand_angle), math.sin(stand_angle)   # 홍학 몸통 방향
            vx, vy = math.cos(aim_angle), math.sin(aim_angle)       # 마우스 방향

            # 공 옆에 오는 것은 머리가 아니라 '발 근처'
            foot_origin_dist = self.currentBall.radius + 18
            foot_origin = (
                bx + vx * foot_origin_dist,
                by + vy * foot_origin_dist
            )

            def local(a, b):
                return (
                    foot_origin[0] + ux * a + vx * b,
                    foot_origin[1] + uy * a + vy * b
                )

            # 기본 자세(차징/스윙 전)
            foot1 = local(0, -4)
            foot2 = local(2, 8)

            knee1 = local(18, -3)
            knee2 = local(16, 8)

            body_center = local(48, 1)
            neck_base = local(36, 0)
            neck_mid = local(58, -8)
            head_center = local(78, -10)

            def rotate_point(p, center, ang):
                px, py = p
                cx, cy = center
                rx = px - cx
                ry = py - cy
                return (
                    cx + rx * math.cos(ang) - ry * math.sin(ang),
                    cy + rx * math.sin(ang) + ry * math.cos(ang)
                )

            # 머리를 회전축으로 사용
            tilt_angle = 0

            if self.charging:
                hold_time = pygame.time.get_ticks() - self.mouse_down_time
                hold_ratio = min(hold_time / self.max_hold_time, 1)
                tilt_angle = math.pi * 0.42 * hold_ratio

            elif self.swinging:
                elapsed = pygame.time.get_ticks() - self.swing_start_time
                progress = min(elapsed / self.swing_duration, 1)
                eased = 1 - (1 - progress) * (1 - progress)

                start_tilt = math.pi * 0.42
                end_tilt = -math.pi * 0.22
                tilt_angle = start_tilt + (end_tilt - start_tilt) * eased

            # 머리를 제외한 나머지 부위를 머리 기준으로 회전
            if self.charging or self.swinging:
                foot1 = rotate_point(foot1, head_center, tilt_angle)
                foot2 = rotate_point(foot2, head_center, tilt_angle)
                knee1 = rotate_point(knee1, head_center, tilt_angle)
                knee2 = rotate_point(knee2, head_center, tilt_angle)

            # 정수 좌표로 변환
            foot1 = (int(foot1[0]), int(foot1[1]))
            foot2 = (int(foot2[0]), int(foot2[1]))
            knee1 = (int(knee1[0]), int(knee1[1]))
            knee2 = (int(knee2[0]), int(knee2[1]))
            body_center = (int(body_center[0]), int(body_center[1]))
            neck_base = (int(neck_base[0]), int(neck_base[1]))
            neck_mid = (int(neck_mid[0]), int(neck_mid[1]))
            head_center = (int(head_center[0]), int(head_center[1]))

            # 부리는 공 쪽을 향하게
            beak_angle = math.atan2(by - head_center[1], bx - head_center[0]) + math.pi / 2
            bdx, bdy = math.cos(beak_angle), math.sin(beak_angle)
            bpx, bpy = -math.sin(beak_angle), math.cos(beak_angle)

            beak_tip = (
                int(head_center[0] + bdx * 18),
                int(head_center[1] + bdy * 18)
            )
            beak_left = (
                int(head_center[0] + bdx * 6 + bpx * 5),
                int(head_center[1] + bdy * 6 + bpy * 5)
            )
            beak_right = (
                int(head_center[0] + bdx * 6 - bpx * 5),
                int(head_center[1] + bdy * 6 - bpy * 5)
            )

            eye = (
                int(head_center[0] - bpx * 3),
                int(head_center[1] - bpy * 3)
            )

            # 다리
            pygame.draw.line(self.screen, self.colors["BLACK"], foot1, knee1, 3)
            pygame.draw.line(self.screen, self.colors["BLACK"], knee1, (body_center[0] - 7, body_center[1] + 8), 3)
            pygame.draw.line(self.screen, self.colors["BLACK"], (foot1[0] - 6, foot1[1]), (foot1[0] + 5, foot1[1]), 2)

            pygame.draw.line(self.screen, self.colors["BLACK"], foot2, knee2, 3)
            pygame.draw.line(self.screen, self.colors["BLACK"], knee2, (body_center[0] + 4, body_center[1] + 8), 3)
            pygame.draw.line(self.screen, self.colors["BLACK"], (foot2[0] - 6, foot2[1]), (foot2[0] + 5, foot2[1]), 2)

            # 목
            pygame.draw.lines(
                self.screen,
                self.colors["BLACK"],
                False,
                [body_center, neck_base, neck_mid, head_center],
                9
            )
            
            pygame.draw.lines(
                self.screen,
                self.colors["PINK"],
                False,
                [body_center, neck_base, neck_mid, head_center],
                7
            )

            # 몸통
            body_rect = pygame.Rect(body_center[0] - 17, body_center[1] - 11, 34, 22)
            pygame.draw.ellipse(self.screen, self.colors["PINK"], body_rect)
            pygame.draw.ellipse(self.screen, self.colors["BLACK"], body_rect, 2)

            # 날개
            wing_rect = pygame.Rect(body_center[0] - 10, body_center[1] - 5, 20, 12)
            pygame.draw.arc(self.screen, self.colors["RED"], wing_rect, 0, math.pi, 2)            

            # 부리
            pygame.draw.polygon(
                self.screen,
                self.colors["YELLOW"],
                [beak_left, beak_tip, beak_right]
            )
            pygame.draw.line(self.screen, self.colors["BLACK"], head_center, beak_tip, 1)

            # 머리
            pygame.draw.circle(self.screen, self.colors["PINK"], head_center, 11)
            pygame.draw.circle(self.screen, self.colors["BLACK"], head_center, 11, 2)            

            # 눈
            pygame.draw.circle(self.screen, self.colors["BLACK"], eye, 2)

            # 힘 게이지
            if self.charging:
                hold_time = pygame.time.get_ticks() - self.mouse_down_time
                hold_ratio = min(hold_time / self.max_hold_time, 1)

                bar_x, bar_y = 20, 60
                bar_width, bar_height = 160, 14
                fill_width = int(bar_width * hold_ratio)

                pygame.draw.rect(
                    self.screen,
                    self.colors["BLACK"],
                    pygame.Rect(bar_x, bar_y, bar_width, bar_height),
                    2
                )
                pygame.draw.rect(
                    self.screen,
                    self.colors["ORANGE"],
                    pygame.Rect(bar_x, bar_y, fill_width, bar_height)
                )

        # 배경 그리기
        self.screen.fill(self.colors["GREEN"])

        for x in range(0, self.width, 40):
            pygame.draw.line(self.screen, self.colors["DARK_GREEN"], (x, 0), (x + 80, self.height), 1)

        # 공을 먼저 그림: 골대 뒤로 지나갈 수 있게 하기 위함
        for player in self.players:
            draw_hedgehog_ball(player)

        # 플레이어 차례에는 홍학 채를 항상 표시
        if self.currentPlayer == self.players[0] and not self.isWin and self.currentPlayer.ball.speed == 0:
            draw_flamingo_handle()

        # 골문을 나중에 그림: 공이 골대 뒤로 지나가는 듯한 느낌
        target_goal = self.currentPlayer.passedGoals if not self.isWin else -1

        for i, goalpost in enumerate(self.goalposts):
            draw_goalpost(goalpost, active=(i == target_goal))

        # 현재 턴, 목표, 점수 표시
        player_name = "플레이어" if self.currentPlayer == self.players[0] else "여왕"

        if self.isWin:
            winner_name = "플레이어" if self.winner == self.players[0] else "여왕"
            message = f"{winner_name} 승리!"
        else:
            message = (
                f"{player_name} 차례 / "
                f"현재 목표 : {self.currentPlayer.passedGoals + 1}번 문 / "
                f"플레이어 {self.players[0].passedGoals}개, "
                f"여왕 {self.players[1].passedGoals}개 통과"
            )

        text = self.font.render(message, True, self.colors["BLACK"])
        self.screen.blit(text, (20, 20))

    def run(self):
        running = True

        while running:
            self.clock.tick(60)

            self.currentPlayer = self.players[self.currentTurn % 2]
            self.currentBall = self.currentPlayer.ball

            running = self.currentPlayer.play()
            self.update()
            self.draw()
            pygame.display.flip()

        pygame.quit()