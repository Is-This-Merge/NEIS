from GamePlayer import GamePlayer
from Goalpost import Goalpost
from Soldier import Soldier
from Queen import Queen

import pygame, random, math

class CroquetMatch:
    font = None
    def __init__(self):
        self.currentTurn = 0
        self.isGameOver = False
        self.winner = None

        self.field_width, self.field_height = 3500 // 4, 2500 // 4
        self.ui_height = 125
        self.width = self.field_width
        self.height = self.field_height + self.ui_height

        self.last_assign_msg = ""
        self.last_assign_time = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("이상한 나라의 크로케 경기")
        self.clock = pygame.time.Clock()

        self.goalposts = []
        self.soldiers = []
        self.available_soldiers = [s for s in self.soldiers if s.is_available(self.currentTurn)]

        self.ground = [[(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(self.width)] for _ in range(self.height)]

        center = (self.field_width//2, self.ui_height+self.field_height//2)
        self.players = [
            GamePlayer(self, (center[0] - 40, center[1])),
            Queen(self, (center[0] + 40, center[1]))
        ]

        self.currentPlayer = self.players[0]
        self.currentBall = self.currentPlayer.ball

        # 골문 배치
        for i in range(8):
            while True:
                location = (random.randint(100, self.field_width - 100), random.randint(self.ui_height + 100, self.height - 100))
                is_overlap = False
                for other_goalpost in self.goalposts:
                    ox, oy = other_goalpost.location
                    distance = math.hypot(location[0]-ox, location[1]-oy)
                    if distance < 130:
                        is_overlap = True
                        break
                if not is_overlap:
                    break
            self.goalposts.append(Goalpost(location, i+1))

        # 병사 골대에 배치
        for i in range(16):
            soldier = Soldier(self, self.goalposts[i % 8])
            self.soldiers.append(soldier)

    def set_msg(self, msg):
        self.last_assign_msg= msg
        self.last_assign_time = pygame.time.get_ticks()

    def update(self):
        # 게임오버 시 리턴
        if self.isGameOver:
            return

        # 홍학 스윙 애니메이션 처리
        flamingo = self.currentPlayer.getCurrentFlamingo()
        if flamingo and flamingo.swinging:
            hit_happened = flamingo.update_swing(self.currentBall)
            if hit_happened:
                self.currentBall.rolling = True

        # 공 굴러가기
        self.currentBall.roll()

        goalpost = self.goalposts[self.currentPlayer.passedGoals]
        gx, gy = goalpost.location
        distance = math.hypot(self.currentBall.location[0] - gx, self.currentBall.location[1] - gy)

        # 골 넣음 판정
        if distance < 32 and len(goalpost.soldiers) >= 1:
            self.currentPlayer.passedGoals += 1
            if self.currentPlayer.passedGoals >= len(self.goalposts):
                self.isGameOver = True
                self.winner = self.currentPlayer

        # 공이 멈추면 턴 넘기기
        if self.currentBall.rolling and self.currentBall.speed < 0.1:
            self.currentBall.velocity = (0, 0)
            self.currentBall.speed = 0
            self.currentBall.rolling = False

            flamingo = self.currentPlayer.getCurrentFlamingo()
            flamingo.charging = False
            flamingo.swinging = False

            self.currentTurn += 1

            # 쿨다운이 끝난 병사를 다시 사용 가능 상태로 복귀
            for soldier in self.soldiers:
                soldier.update_cooldown(self.currentTurn)

            self.available_soldiers = [s for s in self.soldiers if s.is_available(self.currentTurn)]

            # 병사가 없는 골대가 4턴 이상 지속되면 플레이어 패배
            for goalpost in self.goalposts:
                if len(goalpost.soldiers) == 0:
                    if goalpost.emptySinceTurn is None:
                        goalpost.emptySinceTurn = self.currentTurn
                    elif self.currentTurn - goalpost.emptySinceTurn >= 4:
                        self.isGameOver = True
                        self.winner = self.players[1]  # 플레이어 패배 → 여왕 승리
                else:
                    goalpost.emptySinceTurn = None

    def draw(self):
        colors = {
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

        def draw_panel(rect):
            pygame.draw.rect(self.screen, colors["WHITE"], rect, border_radius=8)
            pygame.draw.rect(self.screen, colors["BLACK"], rect, 2, border_radius=8)

        def draw_top_ui():
            def draw_hp_bar(x, y, hp, max_hp=100, width=55, height=8):
                ratio = max(0, min(hp / max_hp, 1))
                pygame.draw.rect(self.screen, colors["BLACK"], pygame.Rect(x, y, width, height), 1)
                pygame.draw.rect(self.screen, colors["RED"], pygame.Rect(x + 1, y + 1, int((width - 2) * ratio), height - 2))

            # 홍학 HP 박스
            draw_panel(pygame.Rect(15, 15, 315, 96))

            title = pygame.font.SysFont("malgungothic", 22).render("홍학 HP", True, colors["BLACK"])
            self.screen.blit(title, (30, 22))

            labels = ["플레이어", "하트여왕"]

            for row, player in enumerate(self.players):
                x = 125
                y = 58 + row * 28
                label_text = pygame.font.SysFont("malgungothic", 22).render(labels[row], True, colors["BLACK"])
                self.screen.blit(label_text, (30, y - 12))

                # 현재 사용 중인 홍학의 HP 바 하나만 표시
                flamingo = player.getCurrentFlamingo()            

                # 홍학 머리
                scale = 0.75
                r = int(7 * scale)
                pygame.draw.line(self.screen, colors["PINK"], (x - int(5 * scale), y + int(12 * scale)), (x + int(2 * scale), y), max(2, int(4 * scale)))

                pygame.draw.circle(self.screen, colors["PINK"], (x, y), r)
                pygame.draw.circle(self.screen, colors["BLACK"], (x, y), r, 1)

                pygame.draw.polygon(
                    self.screen,
                    colors["YELLOW"],
                    [
                        (x + int(6 * scale), y - int(3 * scale)),
                        (x + int(18 * scale), y),
                        (x + int(6 * scale), y + int(3 * scale))
                    ]
                )

                pygame.draw.line(self.screen, colors["BLACK"], (x + int(10 * scale), y), (x + int(18 * scale), y), 1)
                pygame.draw.circle(self.screen, colors["BLACK"], (x + int(2 * scale), y - int(3 * scale)), 1)

                draw_hp_bar(x + 18, y - 7, flamingo.hp, 100, 120, 10)

                # 남은 홍학 개수 표시
                remaining = sum(1 for f in player.flamingos if f.usable)
                count_text = pygame.font.SysFont("malgungothic", 22).render(
                    f"{remaining}/{len(player.flamingos)}", True, colors["BLACK"]
                )
                self.screen.blit(count_text, (x + 145, y - 12))

            # 현재 턴 표시
            draw_panel(pygame.Rect(self.width//2-220/ 2, 15, 220, 64))
            turn_number = self.currentTurn + 1
            player_name = "플레이어" if self.currentPlayer == self.players[0] else "하트여왕"
            turn_text = pygame.font.SysFont("malgungothic", 22).render(f"{turn_number}번째 턴", True, colors["BLACK"])
            player_text = pygame.font.SysFont("malgungothic", 22).render(f"{player_name} 차례", True, colors["BLACK"])
            self.screen.blit(turn_text, turn_text.get_rect(center=(self.width // 2, 35)))
            self.screen.blit(player_text, player_text.get_rect(center=(self.width // 2, 61)))

            # 각자의 목표 골대
            draw_panel(pygame.Rect(self.width - 290, 15, 275, 96))
            title = pygame.font.SysFont("malgungothic", 22).render("현재 목표 골대", True, colors["BLACK"])
            self.screen.blit(title, (self.width - 275, 22))
            for row, player in enumerate(self.players):
                y = 58 + row * 28
                if player.passedGoals >= len(self.goalposts):
                    goal_text = "완료"
                else:
                    goal_text = f"{player.passedGoals + 1}번"
                label_text = pygame.font.SysFont("malgungothic", 22).render(f"{labels[row]} : {goal_text}", True, colors["BLACK"])
                self.screen.blit(label_text, (self.width - 275, y - 12))
                # 플레이어 색깔 표시용 작은 원
                pygame.draw.circle(self.screen, player.ball.color, (self.width - 50, y - 2), 8)
                pygame.draw.circle(self.screen, colors["BLACK"], (self.width - 50, y - 2), 8, 2)

            # 게임 오버 메시지
            if self.isGameOver:
                winner_name = "플레이어" if self.winner == self.players[0] else "하트여왕"
                win_text = pygame.font.SysFont("malgungothic", 28).render(f"{winner_name} 승리!", True, colors["BLACK"])
                win_rect = win_text.get_rect(center=(self.width//2, self.ui_height+self.height//2))

                pygame.draw.rect(self.screen, colors["WHITE"], win_rect.inflate(30, 18), border_radius=8)
                pygame.draw.rect(self.screen, colors["BLACK"], win_rect.inflate(30, 18), 2, border_radius=8)
                self.screen.blit(win_text, win_rect)

        # 전체 배경: UI 영역
        self.screen.fill(colors["UI_BG"])

        # 경기장 배경
        field_rect = pygame.Rect(0, self.ui_height, self.width, self.height)
        pygame.draw.rect(self.screen, colors["GREEN"], field_rect)
        pygame.draw.rect(self.screen, colors["BLACK"], field_rect, 3)

        # 경기장 잔디 선
        for x in range(-120, self.field_width, 40):
            pygame.draw.line(self.screen, colors["DARK_GREEN"], (x, self.ui_height), (x + 80, self.height), 1)

        # 공
        for player in self.players:
            player.ball.draw_ball(self.currentPlayer==player)

        def draw_aim_arrow(flamingo):
            bx, by = self.currentPlayer.ball.location

            if flamingo.charging:
                # 차징 중: 충전 시작 시점의 각도를 고정 사용
                aim_angle = flamingo.charge_angle + math.pi
                hold_time = pygame.time.get_ticks() - flamingo.mouse_down_time
                hold_ratio = min(hold_time / flamingo.max_hold_time, 1)
            else:
                # 클릭 전(조준 중): 현재 마우스 위치 기준으로 방향 계산
                mx, my = pygame.mouse.get_pos()
                charge_angle = math.atan2(my - by, mx - bx)
                aim_angle = charge_angle + math.pi
                hold_ratio = 0

            # 화살표 길이는 충전량에 비례
            length = 45 + hold_ratio * 90

            dx, dy = math.cos(aim_angle), math.sin(aim_angle)
            start = (bx + dx * (self.currentPlayer.ball.radius + 6),
                     by + dy * (self.currentPlayer.ball.radius + 6))
            end = (start[0] + dx * length, start[1] + dy * length)

            # 충전량에 따라 색을 노랑 → 주황 → 빨강으로 변화
            color = (255, int(200 * (1 - hold_ratio)), 0)

            # 화살표 몸통
            pygame.draw.line(self.screen, colors["BLACK"], (int(start[0]), int(start[1])), (int(end[0]), int(end[1])), 7)
            pygame.draw.line(self.screen, color, (int(start[0]), int(start[1])), (int(end[0]), int(end[1])), 4)

            # 화살촉
            head_len = 16
            head_angle = math.pi / 6
            left = (end[0] - head_len * math.cos(aim_angle - head_angle),
                    end[1] - head_len * math.sin(aim_angle - head_angle))
            right = (end[0] - head_len * math.cos(aim_angle + head_angle),
                     end[1] - head_len * math.sin(aim_angle + head_angle))

            head_points = [(int(end[0]), int(end[1])),
                           (int(left[0]), int(left[1])),
                           (int(right[0]), int(right[1]))]
            pygame.draw.polygon(self.screen, color, head_points)
            pygame.draw.polygon(self.screen, colors["BLACK"], head_points, 2)

        def draw_goal_status(goalpost):
            gx, gy = goalpost.location
            count = len(goalpost.soldiers)

            # 도움이 필요한 골대를 강조 (0명=빨강, 1명=주황 링이 깜빡임)
            ring = None
            if count == 0:
                ring = colors["RED"]
            elif count == 1:
                ring = colors["ORANGE"]

            if ring is not None:
                pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) / 2
                radius = 42 + int(pulse * 6)
                pygame.draw.circle(self.screen, ring, (gx, gy), radius, 2)

            # 병사 수 표시 (골대 오른쪽)
            count_text = pygame.font.SysFont("malgungothic", 22).render(f"{count}", True, colors["BLACK"])
            count_bg = count_text.get_rect(center=(gx + 36, gy - 30))
            pygame.draw.circle(self.screen, colors["WHITE"], count_bg.center, 11)
            pygame.draw.circle(self.screen, colors["BLACK"], count_bg.center, 11, 1)
            self.screen.blit(count_text, count_text.get_rect(center=count_bg.center))

            # 빈 골대는 득점 불가 + 게임오버까지 남은 턴 안내
            if count == 0:
                if goalpost.emptySinceTurn is not None:
                    remaining = 4 - (self.currentTurn - goalpost.emptySinceTurn)
                    text = f"득점 불가! {max(0, remaining)}턴"
                else:
                    text = "득점 불가"

                warn = pygame.font.SysFont("malgungothic", 22).render(text, True, colors["RED"])
                warn_rect = warn.get_rect(center=(gx, gy + 78))
                pygame.draw.rect(self.screen, colors["WHITE"], warn_rect.inflate(10, 4), border_radius=4)
                self.screen.blit(warn, warn_rect)

        def draw_assign_panel():
            # 플레이어 차례에만 병사 배치 안내 표시
            if self.currentPlayer != self.players[0] or self.isGameOver:
                return

            panel = pygame.Rect(15, self.height - 66, 450, 65)
            draw_panel(panel)
            line1 = pygame.font.SysFont("malgungothic", 22).render(f"배치 가능 병사: {len(self.available_soldiers)}명", True, colors["BLACK"])
            line2 = pygame.font.SysFont("malgungothic", 22).render("숫자키 1~8 : 해당 번호 골대에 병사 배치", True, colors["BLACK"])
            self.screen.blit(line1, (panel.x + 12, panel.y + 4))
            self.screen.blit(line2, (panel.x + 12, panel.y + 26))

            # 배치 직후 피드백 메시지 (1.5초간 표시)
            msg = self.last_assign_msg
            if msg and pygame.time.get_ticks() - self.last_assign_time < 1500:
                feedback = pygame.font.SysFont("malgungothic", 22).render(msg, True, colors["BLUE"])
                fb_rect = feedback.get_rect(midleft=(panel.right + 12, panel.centery))
                pygame.draw.rect(self.screen, colors["WHITE"], fb_rect.inflate(10, 6), border_radius=4)
                self.screen.blit(feedback, fb_rect)

        # 홍학 채를 표시
        flamingo = self.currentPlayer.getCurrentFlamingo()
        if not self.isGameOver and flamingo is not None:
            if self.currentPlayer == self.players[0]:
                # 사람 플레이어: 조준(정지) 중 또는 차징/스윙 중 표시
                if self.currentPlayer.ball.speed == 0 or flamingo.charging or flamingo.swinging:
                    flamingo.draw_flamingo_handle(self.screen, self.currentPlayer.ball)

                # 조준 중(정지) 또는 차징 중에 조준 방향 화살표를 표시
                if flamingo.charging or (self.currentPlayer.ball.speed == 0 and not flamingo.swinging):
                    draw_aim_arrow(flamingo)
            else:
                # 여왕(AI): 스윙 애니메이션이 진행되는 동안만 표시
                if flamingo.swinging:
                    flamingo.draw_flamingo_handle(self.screen, self.currentPlayer.ball)

        # 골문을 나중에 그림
        for goalpost in self.goalposts:
            goalpost.draw_goalpost(self.screen)
            goalpost.draw_goal_markers(self.screen, self.players)
            draw_goal_status(goalpost)

        # 병사 배치 안내 패널
        draw_assign_panel()

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