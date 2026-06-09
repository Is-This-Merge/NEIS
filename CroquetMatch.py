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
        self.isGameOver = False
        self.winner = None

        # 화면 크기: 상단 UI 영역 + 경기장 영역
        self.field_width, self.field_height = 3500 // 4, 2800 // 4
        self.ui_height = 125
        self.width, self.height = self.field_width, self.field_height + self.ui_height
        self.field_offset_x, self.field_offset_y = 0, self.ui_height

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("이상한 나라의 크로케 경기")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("malgungothic", 28)
        self.small_font = pygame.font.SysFont("malgungothic", 22)

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
            "ORANGE": (255, 165, 0),
            "UI_BG": (230, 230, 220)
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

        # 홍학 스윙 애니메이션 상태
        self.swing_start_time = 0
        self.swing_duration = 300
        self.swing_hit_done = False
        self.swing_pending_velocity = (0, 0)
        self.swing_base_angle = 0
        self.flamingo_charge_angle = 0

        self.soldiers = [Soldier(cooldown=0, match=self) for _ in range(self.soldiersNum)]

        # 골문끼리 겹치지 않게 경기장 내부에 배치
        min_goalpost_distance = 130

        for i in range(self.goalpostsNum):
            while True:
                location = (
                    random.randint(100, self.field_width - 100),
                    random.randint(self.field_offset_y + 100, self.height - 100)
                )

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

        self.center = (
            self.field_width // 2,
            self.field_offset_y + self.field_height // 2
        )

        self.players = [
            GamePlayer(self, (self.center[0] - 40, self.center[1])),
            Queen(self, (self.center[0] + 40, self.center[1]))
        ]

        # 공 크기 조금 줄이기
        for player in self.players:
            player.ball.radius = max(8, int(player.ball.radius * 0.75))
            player.ball.speed = 0

        self.currentPlayer = self.players[0]
        self.currentBall = self.currentPlayer.ball

    def update(self):
        if self.isGameOver:
            return

        # 홍학 스윙 애니메이션 처리
        self.max_hold_time = 2000
        self.min_power = 2.5
        self.max_power = self.currentPlayer.flamingos[self.currentPlayer.currentFlamingo].maxDistance*0.12

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

        bx += vx
        by += vy
        vx *= self.friction
        vy *= self.friction

        if abs(vx) < 0.05:
            vx = 0
        if abs(vy) < 0.05:
            vy = 0

        radius = self.currentBall.radius

        # 경기장 경계 튕김
        left_bound = self.field_offset_x
        right_bound = self.field_offset_x + self.field_width
        top_bound = self.field_offset_y
        bottom_bound = self.field_offset_y + self.field_height

        if bx - radius < left_bound or bx + radius > right_bound:
            vx *= -0.8
            bx = max(left_bound + radius, min(right_bound - radius, bx))

        if by - radius < top_bound or by + radius > bottom_bound:
            vy *= -0.8
            by = max(top_bound + radius, min(bottom_bound - radius, by))

        # 골대 충돌 판정: 카드병정의 밑동 부분에만 적용
        for goalpost in self.goalposts:
            gx, gy = goalpost.location

            left_x = gx - 20
            right_x = gx + 20
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
            self.isGameOver = True
            self.winner = self.currentPlayer
            return

        goalpost = self.goalposts[self.currentPlayer.passedGoals]
        gx, gy = goalpost.location
        distance = math.hypot(bx - gx, by - gy)

        if distance < 32:
            self.currentPlayer.passedGoals += 1

            if self.currentPlayer.passedGoals >= len(self.goalposts):
                self.isGameOver = True
                self.winner = self.currentPlayer

        # 공이 멈추면 턴 넘기기
        self.currentBall.speed = math.hypot(*self.currentBall.velocity)

        if self.turnStarted and self.currentBall.speed < 0.1:
            self.currentBall.velocity = (0, 0)
            self.currentBall.speed = 0
            self.turnStarted = False
            self.aiming = False
            self.charging = False
            self.swinging = False
            self.currentTurn += 1

    def draw(self):
        def draw_panel(rect):
            pygame.draw.rect(self.screen, self.colors["WHITE"], rect, border_radius=8)
            pygame.draw.rect(self.screen, self.colors["BLACK"], rect, 2, border_radius=8)

        def draw_flamingo_head_icon(x, y, scale=1):
            r = int(7 * scale)

            pygame.draw.line(
                self.screen,
                self.colors["PINK"],
                (x - int(5 * scale), y + int(12 * scale)),
                (x + int(2 * scale), y),
                max(2, int(4 * scale))
            )

            pygame.draw.circle(self.screen, self.colors["PINK"], (x, y), r)
            pygame.draw.circle(self.screen, self.colors["BLACK"], (x, y), r, 1)

            pygame.draw.polygon(
                self.screen,
                self.colors["YELLOW"],
                [
                    (x + int(6 * scale), y - int(3 * scale)),
                    (x + int(18 * scale), y),
                    (x + int(6 * scale), y + int(3 * scale))
                ]
            )

            pygame.draw.line(self.screen, self.colors["BLACK"], (x + int(10 * scale), y), (x + int(18 * scale), y), 1)
            pygame.draw.circle(self.screen, self.colors["BLACK"], (x + int(2 * scale), y - int(3 * scale)), 1)

        def draw_top_ui():
            def get_flamingo_hp(flamingo):
                return getattr(flamingo, "hp", getattr(flamingo, "HP", getattr(flamingo, "health", 100)))

            def draw_hp_bar(x, y, hp, max_hp=100, width=55, height=8):
                ratio = max(0, min(hp / max_hp, 1))
                pygame.draw.rect(self.screen, self.colors["BLACK"], pygame.Rect(x, y, width, height), 1)
                pygame.draw.rect(self.screen, self.colors["RED"], pygame.Rect(x + 1, y + 1, int((width - 2) * ratio), height - 2))

            # 왼쪽 위: 홍학 HP
            left_panel = pygame.Rect(15, 15, 315, 96)
            draw_panel(left_panel)

            title = self.small_font.render("홍학 HP", True, self.colors["BLACK"])
            self.screen.blit(title, (30, 22))

            labels = ["플레이어", "하트여왕"]

            for row, player in enumerate(self.players):
                y = 58 + row * 28
                label_text = self.small_font.render(labels[row], True, self.colors["BLACK"])
                self.screen.blit(label_text, (30, y - 12))

                for i, flamingo in enumerate(player.flamingos):
                    icon_x = 125 + i * 58
                    hp = get_flamingo_hp(flamingo)

                    draw_flamingo_head_icon(icon_x, y - 2, 0.75)
                    draw_hp_bar(icon_x + 18, y - 7, hp, 100, 34, 8)

                    if i == player.currentFlamingo:
                        pygame.draw.rect(
                            self.screen,
                            self.colors["BLACK"],
                            pygame.Rect(icon_x - 11, y - 18, 61, 28),
                            2,
                            border_radius=4
                        )

            # 위쪽 중앙: 현재 턴
            center_panel_width = 220
            center_panel = pygame.Rect(self.width // 2 - center_panel_width // 2, 15, center_panel_width, 64)
            draw_panel(center_panel)

            turn_number = self.currentTurn + 1
            player_name = "플레이어" if self.currentPlayer == self.players[0] else "하트여왕"

            turn_text = self.small_font.render(f"{turn_number}번째 턴", True, self.colors["BLACK"])
            player_text = self.small_font.render(f"{player_name} 차례", True, self.colors["BLACK"])

            self.screen.blit(turn_text, turn_text.get_rect(center=(self.width // 2, 35)))
            self.screen.blit(player_text, player_text.get_rect(center=(self.width // 2, 61)))

            # 오른쪽 위: 각자의 목표 골대
            right_panel = pygame.Rect(self.width - 290, 15, 275, 96)
            draw_panel(right_panel)

            title = self.small_font.render("현재 목표 골대", True, self.colors["BLACK"])
            self.screen.blit(title, (self.width - 275, 22))

            for row, player in enumerate(self.players):
                y = 58 + row * 28

                if player.passedGoals >= len(self.goalposts):
                    goal_text = "완료"
                else:
                    goal_text = f"{player.passedGoals + 1}번"

                label_text = self.small_font.render(f"{labels[row]} : {goal_text}", True, self.colors["BLACK"])
                self.screen.blit(label_text, (self.width - 275, y - 12))

                # 플레이어 색깔 표시용 작은 원
                pygame.draw.circle(self.screen, player.ball.color, (self.width - 50, y - 2), 8)
                pygame.draw.circle(self.screen, self.colors["BLACK"], (self.width - 50, y - 2), 8, 2)

            if self.isGameOver:
                winner_name = "플레이어" if self.winner == self.players[0] else "하트여왕"
                win_text = self.font.render(f"{winner_name} 승리!", True, self.colors["BLACK"])
                win_rect = win_text.get_rect(center=(self.width // 2, 103))

                pygame.draw.rect(self.screen, self.colors["WHITE"], win_rect.inflate(30, 18), border_radius=8)
                pygame.draw.rect(self.screen, self.colors["BLACK"], win_rect.inflate(30, 18), 2, border_radius=8)
                self.screen.blit(win_text, win_rect)

        def draw_flamingo_handle():
            bx, by = self.currentBall.location
            mx, my = pygame.mouse.get_pos()

            dx = mx - bx
            dy = my - by
            length = math.hypot(dx, dy)

            if length == 0:
                dx, dy = 1, 0
                length = 1

            aim_angle = math.atan2(dy, dx)

            if self.charging or self.swinging:
                aim_angle = self.flamingo_charge_angle

            stand_angle = aim_angle + math.pi / 2

            ux, uy = math.cos(stand_angle), math.sin(stand_angle)
            vx, vy = math.cos(aim_angle), math.sin(aim_angle)

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

            if self.charging or self.swinging:
                foot1 = rotate_point(foot1, head_center, tilt_angle)
                foot2 = rotate_point(foot2, head_center, tilt_angle)
                knee1 = rotate_point(knee1, head_center, tilt_angle)
                knee2 = rotate_point(knee2, head_center, tilt_angle)

            foot1 = (int(foot1[0]), int(foot1[1]))
            foot2 = (int(foot2[0]), int(foot2[1]))
            knee1 = (int(knee1[0]), int(knee1[1]))
            knee2 = (int(knee2[0]), int(knee2[1]))
            body_center = (int(body_center[0]), int(body_center[1]))
            neck_base = (int(neck_base[0]), int(neck_base[1]))
            neck_mid = (int(neck_mid[0]), int(neck_mid[1]))
            head_center = (int(head_center[0]), int(head_center[1]))

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
            pygame.draw.lines(self.screen, self.colors["BLACK"], False, [body_center, neck_base, neck_mid, head_center], 9)
            pygame.draw.lines(self.screen, self.colors["PINK"], False, [body_center, neck_base, neck_mid, head_center], 7)

            # 몸통
            body_rect = pygame.Rect(body_center[0] - 17, body_center[1] - 11, 34, 22)
            pygame.draw.ellipse(self.screen, self.colors["PINK"], body_rect)
            pygame.draw.ellipse(self.screen, self.colors["BLACK"], body_rect, 2)

            # 날개
            wing_rect = pygame.Rect(body_center[0] - 10, body_center[1] - 5, 20, 12)
            pygame.draw.arc(self.screen, self.colors["RED"], wing_rect, 0, math.pi, 2)

            # 부리
            pygame.draw.polygon(self.screen, self.colors["YELLOW"], [beak_left, beak_tip, beak_right])
            pygame.draw.line(self.screen, self.colors["BLACK"], head_center, beak_tip, 1)

            # 머리
            pygame.draw.circle(self.screen, self.colors["PINK"], head_center, 11)
            pygame.draw.circle(self.screen, self.colors["BLACK"], head_center, 11, 2)

            # 눈
            pygame.draw.circle(self.screen, self.colors["BLACK"], eye, 2)

            if self.charging:
                hold_time = pygame.time.get_ticks() - self.mouse_down_time
                hold_ratio = min(hold_time / self.max_hold_time, 1)

                bar_width, bar_height = 54, 8
                bar_x = body_center[0] - bar_width // 2
                bar_y = body_center[1] - 28
                fill_width = int(bar_width * hold_ratio)

                pygame.draw.rect(
                    self.screen,
                    self.colors["WHITE"],
                    pygame.Rect(bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4),
                    border_radius=4
                )

                pygame.draw.rect(
                    self.screen,
                    self.colors["BLACK"],
                    pygame.Rect(bar_x, bar_y, bar_width, bar_height),
                    1
                )

                pygame.draw.rect(
                    self.screen,
                    self.colors["ORANGE"],
                    pygame.Rect(bar_x + 1, bar_y + 1, fill_width, bar_height - 2)
                )

        # 전체 배경: UI 영역
        self.screen.fill(self.colors["UI_BG"])

        # 경기장 배경
        field_rect = pygame.Rect(
            self.field_offset_x,
            self.field_offset_y,
            self.field_width,
            self.field_height
        )

        pygame.draw.rect(self.screen, self.colors["GREEN"], field_rect)
        pygame.draw.rect(self.screen, self.colors["BLACK"], field_rect, 3)

        # 경기장 잔디 선
        for x in range(-120, self.field_width, 40):
            pygame.draw.line(
                self.screen,
                self.colors["DARK_GREEN"],
                (self.field_offset_x + x, self.field_offset_y),
                (self.field_offset_x + x + 80, self.field_offset_y + self.field_height),
                1
            )

        # 공을 먼저 그림: 골대 뒤로 지나갈 수 있게 하기 위함
        for player in self.players:
            self.currentPlayer.ball.draw_hedgehog_ball(player)

        # 플레이어 차례에는 홍학 채를 표시
        if self.currentPlayer == self.players[0] and not self.isGameOver and self.currentPlayer.ball.speed == 0:
            draw_flamingo_handle()

        # 골문을 나중에 그림
        for goalpost in self.goalposts:
            goalpost.draw_goalpost(self.screen)
            goalpost.draw_goal_markers(self.screen, self.players)

        # 상단 UI 표시
        draw_top_ui()

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