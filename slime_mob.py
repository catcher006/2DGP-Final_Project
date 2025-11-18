import time

import game_framework
import random

from player import player_weapon_id
from state_machine import StateMachine
from pico2d import load_image, load_font, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f


# mob Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

time_out = lambda e: e[0] == 'TIMEOUT'

def event_die(e):
    return e[0] == 'DIE'

# 점 (x, y)가 다각형 내부에 있는지 확인하는 함수
def point_in_polygon(x, y, polygon):
    n = len(polygon)
    inside = False

    j = n - 1
    for i in range(n):
        if ((polygon[i][1] > y) != (polygon[j][1] > y)) and \
           (x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            inside = not inside
        j = i

    return inside

class Dead:
    def __init__(self, mob):
        self.mob = mob
        self.max_frame = 5
        self.played = False

    def enter(self, e):
        # 애니메이션을 처음부터 시작하고 이동 정지
        self.mob.frame = 0.0
        self.played = False
        self.mob.dx = 0.0
        self.mob.dy = 0.0

    def exit(self, e):
        pass

    def do(self):
        # 이미 끝났으면 더 이상 진행하지 않음
        if self.played:
            return

        dt = game_framework.frame_time
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        new_frame = self.mob.frame + delta

        if new_frame >= self.max_frame:
            self.mob.frame = float(self.max_frame)
            self.played = True
        else:
            self.mob.frame = new_frame

    def draw(self):
        self.mob.dead_image.clip_draw(int(self.mob.frame) * 30, 0, 30, 26, self.mob.x, self.mob.y, 96, 62)

class Idle:
    def __init__(self, mob):
        self.mob = mob

    def enter(self, e):
        # 방향을 랜덤으로 설정
        self.mob.lr_dir = random.randint(-1, 1)
        if self.mob.lr_dir == 0:
            self.mob.ud_dir = random.choice([-1, 1])
        else:
            self.mob.ud_dir = 0
        self.mob.frame = random.randint(0, 5)
        self.timer = 0.0  # 별도 타이머 추가

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time

        # 타이머 증가
        self.timer += dt

        # 4바퀴 시간 (24프레임 * 0.5초 / 8프레임 = 1.5초)
        if self.timer >= 1.5:
            self.mob.state_machine.handle_state_event(('TIMEOUT', 0))
            return

        # 프레임 애니메이션 (0~5 범위 유지)
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        self.mob.frame = (self.mob.frame + delta) % 6

    def draw(self):
        self.mob.idle_image.clip_draw(int(self.mob.frame) * 48, 0, 48, 31, self.mob.x, self.mob.y, 96, 62)

class Move:
    def __init__(self, mob):
        self.mob = mob

    def enter(self, e):
        self.mob.frame = random.randint(0, 5)
        self.timer = 0.0  # 별도 타이머 추가

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time

        # 타이머 증가
        self.timer += dt

        # 2바퀴 시간 (12프레임 * 0.5초 / 8프레임 = 0.75초)
        if self.timer >= 0.75:
            self.mob.state_machine.handle_state_event(('TIMEOUT', 0))
            return

        # 프레임 애니메이션 (0~5 범위 유지)
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        self.mob.frame = (self.mob.frame + delta) % 6

        # 이동 벡터 계산
        dx = self.mob.lr_dir * RUN_SPEED_PPS * dt
        dy = self.mob.ud_dir * RUN_SPEED_PPS * dt

        self.mob.dx = dx
        self.mob.dy = dy

        new_x = self.mob.x + self.mob.dx
        new_y = self.mob.y + self.mob.dy

        can_move = self.mob.can_move_to(new_x, new_y)

        if can_move:
            self.mob.x = new_x
            self.mob.y = new_y

    def draw(self):
        self.mob.move_image.clip_draw(int(self.mob.frame) * 48, 0, 48, 31, self.mob.x, self.mob.y, 96, 62)

class Slime_Mob:
    def __init__(self):
        self.mob_type = random.choice(["Green", 'Blue', 'Yellow'])

        self.move_image = load_image("./image/mobs/slime/" + self.mob_type + "_Slime_Jump.png")
        self.idle_image = load_image("./image/mobs/slime/" + self.mob_type + "_Slime_Jump.png")
        self.dead_image = load_image("./image/mobs/slime/" + self.mob_type + "_Slime_Dead.png")

        self.font = load_font('ENCR10B.TTF', 16)

        self.x = random.randint(105,940)
        self.y = random.randint(85,540)

        self.frame = random.randint(0,5)
        self.is_move = True

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0  # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0  # left right direction (left: -1, right: 1, none: 0)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.hp = 100  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

        # 데미지 관련 추가
        self.last_damage_time = 0
        self.damage_cooldown = TIME_PER_ACTION

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.DEAD = Dead(self)

        # is_move 값에 따라 초기 상태 결정
        initial_state = self.MOVE if self.is_move else self.IDLE

        # 상태 머신 생성
        self.state_machine = StateMachine(
            initial_state,
            {
                self.MOVE: {time_out: self.IDLE, event_die: Dead(self)},
                self.IDLE: {time_out: self.MOVE, event_die: Dead(self)},
                self.DEAD: {}
            }
        )

    def draw(self):
        self.state_machine.draw()
        if self.mob_type == 'Green':
            self.font.draw(self.x - 35, self.y + 40, f'hp: {self.hp:02d}', (0, 255, 0))
        elif self.mob_type == 'Blue':
            self.font.draw(self.x - 35, self.y + 40, f'hp: {self.hp:02d}', (0, 0, 255))
        elif self.mob_type == 'Yellow':
            self.font.draw(self.x - 35, self.y + 40, f'hp: {self.hp:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        frame = int(self.frame)  # frame을 정수로 변환

        if frame == 0:
            return self.x - 45, self.y - 30, self.x + 30, self.y + 15
        elif frame == 1:
            return self.x - 45, self.y - 32, self.x + 30, self.y + 12
        elif frame == 2:
            return self.x - 38, self.y - 30, self.x + 25, self.y + 24
        elif frame == 3:
            return self.x - 38, self.y - 24, self.x + 25, self.y + 30
        elif frame == 4:
            return self.x - 38, self.y - 30, self.x + 25, self.y + 24
        elif frame == 5:
            return self.x - 48, self.y - 32, self.x + 35, self.y + 12

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def can_move_to(self, x, y):
        if callable(self.move_validator):
            return self.move_validator(x, y)

        return False

    def handle_collision(self, group, other):
        if group == 'player_sword:slime_mob' and self.is_alive:
            current_time = time.time()

            # 마지막 데미지로부터 충분한 시간이 지났는지 확인
            if current_time - self.last_damage_time >= self.damage_cooldown:
                if player_weapon_id == 'normalsword':
                    self.hp -= 10
                elif player_weapon_id == 'silversword':
                    self.hp -= 20
                elif player_weapon_id == 'goldsword':
                    self.hp -= 30
                self.last_damage_time = current_time

                if self.hp <= 0:
                    self.hp = 0
                    self.is_alive = False
                    self.state_machine.handle_state_event(('DIE', None))
                    print("slime_mob is dead!")

                # 디버그 출력 (선택사항)
                print(f"slime_mob damaged! HP: {self.hp}")