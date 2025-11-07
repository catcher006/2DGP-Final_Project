import game_framework
import random
from state_machine import StateMachine
from pico2d import load_image, load_font, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f

class Slime_Mob:
    def __init__(self):
        self.move_image = load_image('./image/mobs/slime/Green_Slime_Jump.png')
        self.idle_image = load_image('./image/mobs/slime/Green_Slime_Idle.png')
        self.dead_image = load_image('./image/mobs/slime/Green_Slime_Dead.png')

        self.x = random.randint(105,940)
        self.y = random.randint(85,540)

        self.frame = 0

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0  # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0  # left right direction (left: -1, right: 1, none: 0)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.hp = 100  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

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