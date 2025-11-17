import time

import game_framework
import stage1_manger
from state_machine import StateMachine
from pico2d import *
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f, SDLK_SPACE

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
FRAMES_PER_DEAD_ACTION = 6

# 모드 호환을 위한 전역 변수 사용
player_hp = 100
player_is_alive = True

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

def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def event_die(e):
    return e[0] == 'DIE'

def space_down(e):  # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


class Dead:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0
        print("Entered Dead state!")  # 디버그용

    def exit(self, e):
        pass

    def do(self):
        if self.player.frame < 5:
            self.player.frame += FRAMES_PER_DEAD_ACTION * ACTION_PER_TIME * game_framework.frame_time


    def draw(self):
        self.player.dead_image.clip_draw(int(self.player.frame) * 64, 0, 64, 64, self.player.x, self.player.y, 100, 100)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass
    def exit(self, e):
        pass

    def do(self):
        if self.player.ydir == 1:
            self.player.face_dir = 3
        elif self.player.xdir == -1:
            self.player.face_dir = 2
        elif self.player.ydir == -1:
            self.player.face_dir = 1
        elif self.player.xdir == 1:
            self.player.face_dir = 0

        self.player.frame = (self.player.frame + FRAMES_PER_IDLE_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2


    def draw(self):
        self.player.idle_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64,self.player.x, self.player.y, 100, 100)


class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time
        # 이동 벡터를 먼저 계산 (px per second * dt)
        dx = self.player.xdir * RUN_SPEED_PPS * dt
        dy = self.player.ydir * RUN_SPEED_PPS * dt

        # 디버깅용으로 player에 저장해두면 유용
        self.player.dx = dx
        self.player.dy = dy

        new_x = self.player.x + self.player.dx
        new_y = self.player.y + self.player.dy

        # print(f"Trying to move to ({new_x}, {new_y})")

        # 실제 이동 가능 여부 검사
        can_move = self.player.can_move_to(new_x, new_y)

        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9

        if can_move:
            self.player.x = new_x
            self.player.y = new_y

    def draw(self):
        if self.player.ydir == 1: self.player.face_dir = 3
        elif self.player.xdir == -1: self.player.face_dir = 2
        elif self.player.ydir == -1: self.player.face_dir = 1
        elif self.player.xdir == 1: self.player.face_dir = 0
        self.player.walk_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64,self.player.x, self.player.y, 100, 100)


class Sword:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.is_attacking = True
        self.player.attack_start_time = time.time()
        self.player.frame = 0

    def exit(self, e):
        self.player.is_attacking = False

    def do(self):
        # 공격 애니메이션 처리
        if self.player.frame < 5:
            self.player.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
        else:
            # 공격 애니메이션이 끝나면 대기 상태로 전환
            self.player.state_machine.handle_state_event(('STOP', None))

    def draw(self):
        self.player.sword_image.clip_draw(int(self.player.frame) * 128, 128 * self.player.face_dir, 128, 128, self.player.x, self.player.y, 200, 200)

class Player:
    def __init__(self):
        self.walk_image = load_image('player_none_none_walk.png')
        self.idle_image = load_image('player_none_none_idle.png')
        self.dead_image = load_image('player_none_none_dead.png')
        self.sword_image = load_image('player_none_normalsword_attack.png')

        self.font = load_font('ENCR10B.TTF', 16)

        self.x = 510
        self.y = 160

        self.frame = 0

        self.dx = 0.0
        self.dy = 0.0

        self.xdir = 0 # up down direction (up: 1, down: -1, none: 0)
        self.ydir = 0 # left right direction (left: -1, right: 1, none: 0)

        self.face_dir = 0 # 마지막 방향 저장 (0: 오른쪽, 1: 아래, 2: 왼쪽, 3: 위)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.is_attacking = False  # 공격 상태
        self.attack_start_time = 0  # 공격 시작 시간

        # 데미지 관련 추가
        self.last_damage_time = 0
        self.damage_cooldown = TIME_PER_ACTION * 3

        # 상태들 생성
        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.DEAD = Dead(self)
        self.SWORD = Sword(self)

        # 상태 머신 생성
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: { event_run: self.WALK, space_down: self.SWORD, event_die: self.DEAD },
                self.WALK: { event_stop: self.IDLE, space_down: self.SWORD, event_die: self.DEAD },
                self.SWORD: { event_stop: self.IDLE, event_die: self.DEAD },
                self.DEAD: {}
            }

        )

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 35, self.y + 40, f'hp: {player_hp:02d}', (0, 0, 255))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.face_dir == 3:
            return self.x - 22, self.y - 47, self.x + 22, self.y + 25
        elif self.face_dir == 2:
            return self.x - 15, self.y - 47, self.x + 15, self.y + 25
        elif self.face_dir == 1:
            return self.x - 22, self.y - 47, self.x + 22, self.y + 25
        elif self.face_dir == 0:
            return self.x - 18, self.y - 47, self.x + 15, self.y + 25

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 죽었으면 입력 무시
        if not player_is_alive:
            return

        if event.key in (SDLK_a, SDLK_d, SDLK_w, SDLK_s):
            cur_xdir, cur_ydir = self.xdir, self.ydir
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_a: self.xdir -= 1
                elif event.key == SDLK_d: self.xdir += 1
                elif event.key == SDLK_w: self.ydir += 1
                elif event.key == SDLK_s: self.ydir -= 1
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_a: self.xdir += 1
                elif event.key == SDLK_d: self.xdir -= 1
                elif event.key == SDLK_w: self.ydir -= 1
                elif event.key == SDLK_s: self.ydir += 1
            if cur_xdir != self.xdir or cur_ydir != self.ydir:  # 방향키에 따른 변화가 있으면
                if self.xdir == 0 and self.ydir == 0:  # 멈춤
                    self.state_machine.handle_state_event(('STOP', self.face_dir))  # 스탑 시 이전 방향 전달
                else:  # 움직임
                    self.state_machine.handle_state_event(('RUN', None))
        else:
            # 공격키일 때 현재 공격 가능 여부 확인
            if space_down(('INPUT', event)) and not stage1_manger.stage1_in_game:
                return
            self.state_machine.handle_state_event(('INPUT', event))

    def can_move_to(self, x, y):
        if callable(self.move_validator):
            return self.move_validator(x, y)

        return False

    def handle_collision(self, group, other):
        global player_hp, player_is_alive

        if group == 'player:slime_mob' and player_is_alive:
            current_time = time.time()

            # 마지막 데미지로부터 충분한 시간이 지났는지 확인
            if current_time - self.last_damage_time >= self.damage_cooldown:
                player_hp -= 10
                self.last_damage_time = current_time

                if player_hp <= 0:
                    player_is_alive = False
                    self.state_machine.handle_state_event(('DIE', None))
                    print("Player is dead!")

                # 디버그 출력 (선택사항)
                print(f"Player damaged! HP: {player_hp}")
