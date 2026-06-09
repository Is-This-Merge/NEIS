from Object import Object

import pygame
import math, random


class Flamingo(Object):
    def __init__(self, match):
        super().__init__()

        self.match = match

        self.hp = 100
        self.maxDistance = random.randint(9, 15)
        self.__stiffness = random.randint(70, 100)

        # 조작 관련
        self.charging = False
        self.swinging = False
        self.mouse_down_time = 0

        # 애니메이션 관련
        self.swing_start_time = 0
        self.swing_hit_done = False
        self.swing_pending_velocity = (0, 0)
        self.charge_angle = 0

        # 차징 관련
        self.max_hold_time = 2000

    def hit(self, hedgehog, strength):
        damage = hedgehog.sharpness * strength / 5 * (1 - self.__stiffness / 100)
        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            self.usable = False

    def start_charge(self, ball):
        if not self.usable:
            return

        bx, by = ball.location
        mx, my = pygame.mouse.get_pos()

        self.charging = True
        self.swinging = False
        self.mouse_down_time = pygame.time.get_ticks()
        self.charge_angle = math.atan2(my - by, mx - bx)

    def release_charge(self):
        if not self.charging or not self.usable:
            return

        hold_time = pygame.time.get_ticks() - self.mouse_down_time
        hold_ratio = min(hold_time / self.max_hold_time, 1)

        power = 7 + (self.maxDistance) * hold_ratio
        angle = self.charge_angle

        #반대쪽으로 발사
        self.swing_pending_velocity = (
            -math.cos(angle) * power * 3,
            -math.sin(angle) * power * 3
        )

        self.swing_start_time = pygame.time.get_ticks()
        self.swing_hit_done = False
        self.swinging = True
        self.charging = False

        return power

    def update_swing(self, ball):
        if not self.swinging:
            return False

        # swing은 애니메이션임
        elapsed = pygame.time.get_ticks() - self.swing_start_time
        progress = min(elapsed / 300, 1)

        if progress >= 0.55 and not self.swing_hit_done:
            ball.velocity = self.swing_pending_velocity
            self.swing_hit_done = True
            return True

        if progress >= 1:
            self.swinging = False

        return False

    def draw_flamingo_handle(self, screen, ball):
        bx, by = ball.location
        mx, my = pygame.mouse.get_pos()

        dx = mx - bx
        dy = my - by

        aim_angle = math.atan2(dy, dx)

        if self.charging or self.swinging:
            aim_angle = self.charge_angle

        stand_angle = aim_angle + math.pi / 2

        ux, uy = math.cos(stand_angle), math.sin(stand_angle)
        vx, vy = math.cos(aim_angle), math.sin(aim_angle)

        # 공 옆에는 홍학의 발이 오도록 함
        foot_origin_dist = ball.radius + 18
        foot_origin = (
            bx + vx * foot_origin_dist,
            by + vy * foot_origin_dist
        )

        def local(a, b):
            return (
                foot_origin[0] + ux * a + vx * b,
                foot_origin[1] + uy * a + vy * b
            )

        # 기본 자세
        foot1 = local(0, -5)
        foot2 = local(2, 9)
        knee1 = local(18, -4)
        knee2 = local(17, 9)

        body_center = local(48, 1)
        neck_base = local(42, 0)
        neck_mid = local(62, -8)
        head_center = local(82, -10)

        def rotate_point(p, center, angle):
            px, py = p
            cx, cy = center
            rx = px - cx
            ry = py - cy

            return (
                cx + rx * math.cos(angle) - ry * math.sin(angle),
                cy + rx * math.sin(angle) + ry * math.cos(angle)
            )

        tilt_angle = 0

        if self.charging:
            hold_time = pygame.time.get_ticks() - self.mouse_down_time
            hold_ratio = min(hold_time / self.max_hold_time, 1)
            tilt_angle = math.pi * 0.42 * hold_ratio

        elif self.swinging:
            elapsed = pygame.time.get_ticks() - self.swing_start_time
            progress = min(elapsed / 300, 1)
            eased = 1 - (1 - progress) * (1 - progress)

            start_tilt = math.pi * 0.42
            end_tilt = -math.pi * 0.22
            tilt_angle = start_tilt + (end_tilt - start_tilt) * eased

        # 머리는 고정하고 나머지만 머리 기준으로 회전
        if self.charging or self.swinging:
            foot1 = rotate_point(foot1, head_center, tilt_angle)
            foot2 = rotate_point(foot2, head_center, tilt_angle)
            knee1 = rotate_point(knee1, head_center, tilt_angle)
            knee2 = rotate_point(knee2, head_center, tilt_angle)
            body_center = rotate_point(body_center, head_center, tilt_angle)
            neck_base = rotate_point(neck_base, head_center, tilt_angle)
            neck_mid = rotate_point(neck_mid, head_center, tilt_angle)

        foot1 = (int(foot1[0]), int(foot1[1]))
        foot2 = (int(foot2[0]), int(foot2[1]))
        knee1 = (int(knee1[0]), int(knee1[1]))
        knee2 = (int(knee2[0]), int(knee2[1]))
        body_center = (int(body_center[0]), int(body_center[1]))
        neck_base = (int(neck_base[0]), int(neck_base[1]))
        neck_mid = (int(neck_mid[0]), int(neck_mid[1]))
        head_center = (int(head_center[0]), int(head_center[1]))


        beak_angle = math.atan2(by - head_center[1], bx - head_center[0])
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

        black = (0, 0, 0)
        pink = (255, 105, 180)
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        white = (255, 255, 255)
        orange = (255, 165, 0)

        # 다리
        pygame.draw.line(screen, black, foot1, knee1, 3)
        pygame.draw.line(screen, black, knee1, (body_center[0] - 7, body_center[1] + 8), 3)
        pygame.draw.line(screen, black, (foot1[0] - 6, foot1[1]), (foot1[0] + 5, foot1[1]), 2)

        pygame.draw.line(screen, black, foot2, knee2, 3)
        pygame.draw.line(screen, black, knee2, (body_center[0] + 4, body_center[1] + 8), 3)
        pygame.draw.line(screen, black, (foot2[0] - 6, foot2[1]), (foot2[0] + 5, foot2[1]), 2)

        # 목
        pygame.draw.lines(screen, black, False, [body_center, neck_base, neck_mid, head_center], 9)
        pygame.draw.lines(screen, pink, False, [body_center, neck_base, neck_mid, head_center], 7)

        # 몸통
        body_rect = pygame.Rect(body_center[0] - 17, body_center[1] - 11, 34, 22)
        pygame.draw.ellipse(screen, pink, body_rect)
        pygame.draw.ellipse(screen, black, body_rect, 2)

        # 날개
        wing_rect = pygame.Rect(body_center[0] - 10, body_center[1] - 5, 20, 12)
        pygame.draw.arc(screen, red, wing_rect, 0, math.pi, 2)

        # 부리
        pygame.draw.polygon(screen, yellow, [beak_left, beak_tip, beak_right])
        pygame.draw.line(screen, black, head_center, beak_tip, 1)

        # 머리
        pygame.draw.circle(screen, pink, head_center, 11)
        pygame.draw.circle(screen, black, head_center, 11, 2)

        # 눈
        pygame.draw.circle(screen, black, eye, 2)

        # 차징 게이지: 홍학 몸통 근처
        if self.charging:
            hold_time = pygame.time.get_ticks() - self.mouse_down_time
            hold_ratio = min(hold_time / self.max_hold_time, 1)

            bar_width, bar_height = 54, 8
            bar_x = body_center[0] - bar_width // 2
            bar_y = body_center[1] - 28
            fill_width = int(bar_width * hold_ratio)

            pygame.draw.rect(
                screen,
                white,
                pygame.Rect(bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4),
                border_radius=4
            )

            pygame.draw.rect(
                screen,
                black,
                pygame.Rect(bar_x, bar_y, bar_width, bar_height),
                1
            )

            pygame.draw.rect(
                screen,
                orange,
                pygame.Rect(bar_x + 1, bar_y + 1, fill_width, bar_height - 2)
            )