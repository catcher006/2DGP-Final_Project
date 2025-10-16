import time
from state_machine import StateMachine
from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s

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

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dx = 0
        self.player.dy = 0
        self.player.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 2

    def draw(self):
        direction_map = {'up': 3, 'left': 2, 'down': 1, 'right': 0}
        row = direction_map[self.player.direction]
        self.player.idle_image.clip_draw(self.player.frame * 64, 64 * row, 64, 64,self.player.x, self.player.y, 100, 100)


class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        speed = 10  # 이동 속도

        if a_down(e) or d_up(e):
            self.player.direction = 'left'
            self.player.dx = -speed
            self.player.dy = 0
        elif d_down(e) or a_up(e):
            self.player.direction = 'right'
            self.player.dx = speed
            self.player.dy = 0
        elif w_down(e) or s_up(e):
            self.player.direction = 'up'
            self.player.dx = 0
            self.player.dy = speed
        elif s_down(e) or w_up(e):
            self.player.direction = 'down'
            self.player.dx = 0
            self.player.dy = -speed

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 9

        new_x = self.player.x + self.player.dx
        new_y = self.player.y + self.player.dy

        can_move = False
        for path in self.player.village_paths:
            if (path['min_x'] <= new_x <= path['max_x'] and path['min_y'] <= new_y <= path['max_y']):
                can_move = True
                break

        if can_move:
            self.player.x = new_x
            self.player.y = new_y

    def draw(self):
        direction_map = {'up': 3, 'left': 2, 'down': 1, 'right': 0}
        row = direction_map[self.player.direction]
        self.player.walk_image.clip_draw(self.player.frame * 64, 64 * row, 64, 64,self.player.x, self.player.y, 100, 100)

class Player:
    def __init__(self):
        self.walk_image = load_image('player_none_none_walk.png')
        self.idle_image = load_image('player_none_none_idle.png')
        self.dead_image = load_image('player_none_none_dead.png')

        self.x = 510
        self.y = 160

        self.frame = 0

        self.dx = 0
        self.dy = 0
        self.direction = 'down'

        # 마을의 이동 가능 통로 영역
        self.village_paths = [
            {'min_x': 10, 'max_x': 1014, 'min_y': 150, 'max_y': 200},  # 중앙 메인 통로 - 1구역 - 전체 해당 부분
            {'min_x': 10, 'max_x': 155, 'min_y': 140, 'max_y': 200},  # 중앙 메인 통로 - 2구역 - 좌측 돌부리 부분
            {'min_x': 645, 'max_x': 1014, 'min_y': 140, 'max_y': 200},  # 중앙 메인 통로 - 3구역 - 우측 표지판 이후 부분
            {'min_x': 155, 'max_x': 225, 'min_y': 150, 'max_y': 200},  # 중앙 메인 통로 - 4구역 - 좌측 돌부리 옆 일부 풀밭 부분
            {'min_x': 370, 'max_x': 520, 'min_y': 60, 'max_y': 120},  # 하단 중앙 통로
            {'min_x': 150, 'max_x': 200, 'min_y': 200, 'max_y': 250},  # 상단 죄측 통로
            {'min_x': 710, 'max_x': 735, 'min_y': 200, 'max_y': 250},  # 상단 우측 통로
        ]

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