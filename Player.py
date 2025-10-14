import time
from state_machine import StateMachine
from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE

def move_key_down(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and
            e[1].key in [SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT])

def move_key_up(e):
    return (e[0] == 'INPUT' and e[1].type == SDL_KEYUP and
            e[1].key in [SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT])

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def attack_end(e):
    return e[0] == 'ATTACK_END'

def player_die(e):
    return e[0] == 'PLAYER_DIE'

def no_move_keys_pressed(e):
    return e[0] == 'NO_MOVE_KEYS'

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dx = 0
        self.player.dy = 0
        self.player.frame = 0
        self.player.idle_frame_counter = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.idle_frame_counter += 1
        if self.player.idle_frame_counter >= self.player.idle_frame_delay:
            self.player.frame = (self.player.frame + 1) % 2
            self.player.idle_frame_counter = 0

    def draw(self):
        direction_map = {'up': 3, 'left': 2, 'down': 1, 'right': 0}
        row = direction_map[self.player.direction]
        self.player.idle_image.clip_draw(
            self.player.frame * 64, 64 * row, 64, 64,
            self.player.x, self.player.y, 100, 100
        )


class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

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


class Attack:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.is_attacking = True
        self.player.attack_start_time = get_time()
        self.player.dx = 0
        self.player.dy = 0

    def exit(self, e):
        self.player.is_attacking = False

    def do(self):
        # 공격 지속 시간 체크 (예: 0.5초)
        if get_time() - self.player.attack_start_time > 0.5:
            self.player.state_machine.handle_state_event(('ATTACK_END', None))

    def draw(self):
        # 공격 애니메이션 구현 (임시로 idle 이미지 사용)
        direction_map = {'up': 3, 'left': 2, 'down': 1, 'right': 0}
        row = direction_map[self.player.direction]
        self.player.idle_image.clip_draw(0, 64 * row, 64, 64, self.player.x, self.player.y, 100, 100)


class Dead:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dx = 0
        self.player.dy = 0
        self.player.is_alive = False

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        self.player.dead_image.clip_draw(0, 0, 64, 64, self.player.x, self.player.y, 100, 100)


class Player:
    def __init__(self):
        self.walk_image = load_image('player_none_none_walk.png')
        self.idle_image = load_image('player_none_none_idle.png')
        self.dead_image = load_image('player_none_none_dead.png')

        self.x = 510
        self.y = 160

        self.frame = 0
        self.idle_frame_counter = 0  # idle 애니메이션용 카운터
        self.idle_frame_delay = 10  # 10프레임마다 idle 프레임 변경

        self.dx = 0
        self.dy = 0
        self.direction = 'down'

        # 현재 눌린 키들을 추적
        self.pressed_keys = set()

        # 마을의 4개 통로 영역
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
        self.ATTACK = Attack(self)
        self.DEAD = Dead(self)

        # 상태 머신 생성
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {
                    move_key_down: self.WALK,
                    space_down: self.ATTACK,
                    player_die: self.DEAD
                },
                self.WALK: {
                    no_move_keys_pressed: self.IDLE,
                    space_down: self.ATTACK,
                    player_die: self.DEAD
                },
                self.ATTACK: {
                    attack_end: self.IDLE,
                    player_die: self.DEAD
                },
                self.DEAD: {}
            }
        )

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

        # 움직임 키가 모두 떼어졌는지 체크
        if not self.pressed_keys and (self.dx != 0 or self.dy != 0):
            self.state_machine.handle_state_event(('NO_MOVE_KEYS', None))

    def handle_event(self, event):
        # 키 추적 업데이트
        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
            self._update_movement()
        elif event.type == SDL_KEYUP:
            self.pressed_keys.discard(event.key)
            self._update_movement()

        self.state_machine.handle_state_event(('INPUT', event))

    def _update_movement(self):
        """현재 눌린 키들을 바탕으로 이동 방향 업데이트"""
        from sdl2 import SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT

        dx, dy = 0, 0

        if SDLK_UP in self.pressed_keys:
            dy = 2
            self.direction = 'up'
        elif SDLK_DOWN in self.pressed_keys:
            dy = -2
            self.direction = 'down'

        if SDLK_LEFT in self.pressed_keys:
            dx = -2
            self.direction = 'left'
        elif SDLK_RIGHT in self.pressed_keys:
            dx = 2
            self.direction = 'right'

        self.dx = dx
        self.dy = dy

    def take_damage(self, damage):
        """체력 감소 및 죽음 처리"""
        self.hp -= damage
        if self.hp <= 0:
            self.state_machine.handle_state_event(('PLAYER_DIE', None))