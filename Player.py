import time
from state_machine import StateMachine
from pico2d import load_image, get_time
from LocationManager import location_manager
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s

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

        print(f"Trying to move to ({new_x}, {new_y})")

        # 현재 위치에 따라 다른 경로 사용
        current_paths = self.player.get_current_paths()

        can_move = False
        for path in current_paths:
            if path['type'] == 'rect':
                if (path['min_x'] <= new_x <= path['max_x'] and
                        path['min_y'] <= new_y <= path['max_y']):
                    can_move = True
                    break
            elif path['type'] == 'polygon':
                if point_in_polygon(new_x, new_y, path['points']):
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
            {'type': 'rect', 'min_x': 10, 'max_x': 1014, 'min_y': 120, 'max_y': 190},  # 중앙 메인 통로 - 가로구역
            {'type': 'rect', 'min_x': 480, 'max_x': 590, 'min_y': 40, 'max_y': 380},  # 중앙 메인 통로 - 세로구역
            {'type': 'polygon', 'points': [
                (190, 190),  # 하단 왼쪽
                (270, 190),  # 하단 오른쪽
                (260, 210),  # 상단 오른쪽
                (210, 210)  # 상단 왼쪽
            ]}, # 집 입구 통로
            {'type': 'polygon', 'points': [
                (730, 190),  # 하단 왼쪽
                (800, 190),  # 하단 오른쪽
                (810, 220),  # 상단 오른쪽
                (770, 230)  # 상단 왼쪽
            ]} # 상점 입구 통로
        ]

        self.house_paths = []

        self.shop_paths = []

        self.dungeon_main_paths = []

        self.dungeon_inside_paths = []

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

    # 현재 위치에 따른 이동 경로 반환
    def get_current_paths(self):
        if location_manager.is_village():
            return self.village_paths
        elif location_manager.is_house():
            return self.house_paths
        elif location_manager.is_shop():
            return self.shop_paths
        elif location_manager.is_dungeon_main():
            return self.dungeon_main_paths
        elif location_manager.is_dungeon_inside():
            return self.dungeon_inside_paths
        else:
            return self.village_paths  # 기본값

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))