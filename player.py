import time

import game_framework
from state_machine import StateMachine
from pico2d import load_image, load_font, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_IDLE_ACTION = 2

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

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f

def f_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_f

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass
    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_IDLE_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2


    def draw(self):
        row = 0
        if self.player.ud_dir == 1:
            row = 3
        elif self.player.lr_dir == -1:
            row = 2
        elif self.player.ud_dir == -1:
            row = 1
        elif self.player.lr_dir == 1:
            row = 0
        self.player.idle_image.clip_draw(int(self.player.frame) * 64, 64 * row, 64, 64,self.player.x, self.player.y, 100, 100)


class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if a_down(e) or d_up(e):
            self.player.ud_dir = 0
            self.player.lr_dir = -1
        elif d_down(e) or a_up(e):
            self.player.ud_dir = 0
            self.player.lr_dir = 1
        elif w_down(e) or s_up(e):
            self.player.ud_dir = 1
            self.player.lr_dir = 0
        elif s_down(e) or w_up(e):
            self.player.ud_dir = -1
            self.player.lr_dir = 0
        elif f_down(e):
            pass

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time
        # 이동 벡터를 먼저 계산 (px per second * dt)
        dx = self.player.lr_dir * RUN_SPEED_PPS * dt
        dy = self.player.ud_dir * RUN_SPEED_PPS * dt

        # 디버깅용으로 player에 저장해두면 유용
        self.player.dx = dx
        self.player.dy = dy

        new_x = self.player.x + self.player.dx
        new_y = self.player.y + self.player.dy

        print(f"Trying to move to ({new_x}, {new_y})")

        # 실제 이동 가능 여부 검사
        can_move = self.player.can_move_to(new_x, new_y)

        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9

        if can_move:
            self.player.x = new_x
            self.player.y = new_y

    def draw(self):
        row = 0
        if self.player.ud_dir == 1: row = 3
        elif self.player.lr_dir == -1: row = 2
        elif self.player.ud_dir == -1: row = 1
        elif self.player.lr_dir == 1: row = 0
        self.player.walk_image.clip_draw(int(self.player.frame) * 64, 64 * row, 64, 64,self.player.x, self.player.y, 100, 100)

class Player:
    def __init__(self):
        self.walk_image = load_image('player_none_none_walk.png')
        self.idle_image = load_image('player_none_none_idle.png')
        self.dead_image = load_image('player_none_none_dead.png')

        self.x = 510
        self.y = 160

        self.frame = 0

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0 # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0 # left right direction (left: -1, right: 1, none: 0)

        self.move_door = 0
        # 이동한 문 위치 (0: 상단, 1: 하단, 2: 좌측, 3: 우측)
        # 4: 던전메인_스테이지1_입구
        # 5: 던전메인_스테이지2_입구
        # 6: 던전메인_스테이지3_입구
        # 7: 던전메인_입구
        # 8: 던전_입구 (마을)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.is_attacking = False  # 공격 상태
        self.attack_start_time = 0  # 공격 시작 시간
        self.hp = 100  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

        # 상태들 생성
        self.IDLE = Idle(self)
        self.WALK = Walk(self)

        # 상태 머신 생성
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {a_down: self.WALK, a_up: self.WALK, d_down: self.WALK, d_up: self.WALK, w_down: self.WALK, w_up: self.WALK, s_down: self.WALK, s_up: self.WALK},
                self.WALK: {a_down: self.IDLE, a_up: self.IDLE, d_down: self.IDLE, d_up: self.IDLE, w_down: self.IDLE, w_up: self.IDLE, s_down: self.IDLE, s_up: self.IDLE}
            }

        )

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def can_move_to(self, x, y):
        if callable(self.move_validator):
            return self.move_validator(x, y)

        return False