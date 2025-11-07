import game_framework
import random
from state_machine import StateMachine
from pico2d import load_image, load_font, get_time
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

class Idle:
    def __init__(self, mob):
        self.mob = mob

    def enter(self, e):
        pass
    def exit(self, e):
        pass

    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1

    def draw(self):
        self.mob.idle_image.clip_draw(int(self.mob.frame) * 38, 0, 38, 23, self.mob.x, self.mob.y, 64, 48)

class Move:
    def __init__(self, mob):
        self.mob = mob

    def enter(self, e):
        pass
    def exit(self, e):
        pass

    def do(self):
        self.mob.frame = (self.mob.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

    def draw(self):
        self.mob.move_image.clip_draw(int(self.mob.frame) * 48, 0, 48, 31, self.mob.x, self.mob.y, 96, 62)

class Slime_Mob:
    def __init__(self):
        self.move_image = load_image('./image/mobs/slime/Green_Slime_Jump.png')
        self.idle_image = load_image('./image/mobs/slime/Green_Slime_Idle.png')
        self.dead_image = load_image('./image/mobs/slime/Green_Slime_Dead.png')

        self.x = random.randint(105,940)
        self.y = random.randint(85,540)

        self.frame = random.randint(0,5)

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0  # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0  # left right direction (left: -1, right: 1, none: 0)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.hp = 100  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

        self.IDLE = Idle(self)
        self.MOVE = Move(self)

        # 상태 머신 생성
        self.state_machine = StateMachine(
            self.MOVE,
            {}
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