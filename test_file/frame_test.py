import game_framework
import random
from state_machine import StateMachine
from pico2d import load_image, load_font, get_time, draw_rectangle, open_canvas, clear_canvas, update_canvas, \
    close_canvas
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f

class Attack:
    def __init__(self, mob):
        self.mob = mob

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        self.mob.image.clip_draw(int(self.mob.frame) * 192, 192 * self.mob.face_dir, 192, 192, self.mob.x, self.mob.y, 600, 600)

class Slime_Mob:
    def __init__(self):
        self.image = load_image("../image/mobs/goblin_boss/attack.png")

        self.x = 600
        self.y = 400

        self.frame = 5
        self.face_dir = 3

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0  # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0  # left right direction (left: -1, right: 1, none: 0)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.hp = 100  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

        self.ATTACK = Attack(self)

        self.state_machine = StateMachine(
            self.ATTACK,
            {}
        )

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())  # 충돌박스 그리기

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def can_move_to(self, x, y):
        if callable(self.move_validator):
            return self.move_validator(x, y)

        return False

    def get_bb(self):
        # face_dir = 0
        # return self.x + 26, self.y - 100, self.x + 138, self.y - 38 # frame : 0
        # return self.x + 16, self.y - 64, self.x + 50, self.y - 38  # frame : 1
        # return self.x - 70, self.y - 50, self.x + 24, self.y - 10  # frame : 2
        # return self.x - 98, self.y - 44, self.x + 54, self.y - 4  # frame : 3
        # return self.x + 44, self.y - 44, self.x + 252, self.y + 34  # frame : 4
        # return self.x + 56, self.y + 6, self.x + 248, self.y + 34  # frame : 5
        # face_dir = 1
        # return self.x - 76, self.y - 104, self.x + 34, self.y - 42 # frame : 0
        # return self.x - 104, self.y - 54, self.x + 16, self.y - 38  # frame : 1
        # return self.x - 100, self.y - 50, self.x - 12, self.y + 36  # frame : 2
        # return self.x - 124, self.y - 66, self.x + 18, self.y + 32  # frame : 3
        # return self.x - 134, self.y - 154, self.x + 120, self.y - 34  # frame : 4
        # return self.x - 18, self.y - 146, self.x + 198, self.y - 18  # frame : 5
        # face_dir = 2
        # return self.x - 138, self.y - 100, self.x - 26, self.y - 38 # frame : 0
        # return self.x - 50, self.y - 64, self.x - 16, self.y - 38  # frame : 1
        # return self.x - 24, self.y - 50, self.x + 70, self.y - 10  # frame : 2
        # return self.x - 54, self.y - 44, self.x + 98, self.y - 4  # frame : 3
        # return self.x - 252, self.y - 44, self.x - 44, self.y + 34  # frame : 4
        # return self.x - 248, self.y + 6, self.x - 56, self.y + 34  # frame : 5
        # face_dir = 3
        # return self.x - 76, self.y - 54, self.x + 34, self.y + 8 # frame : 0
        # return self.x - 104, self.y - 48, self.x + 16, self.y - 32  # frame : 1
        # return self.x - 100, self.y - 80, self.x - 12, self.y + 6  # frame : 2
        # return self.x - 134, self.y - 74, self.x + 8, self.y + 24  # frame : 3
        # return self.x - 134, self.y - 8, self.x + 120, self.y + 112  # frame : 4
        return self.x - 18, self.y - 24, self.x + 198, self.y + 102  # frame : 5





open_canvas(1200,800)

def reset_world():
    global running
    global world # World List - 모든 객체를 갖고 있는 리스트
    global mob

    world = [] # 하나도 객체가 없는 월드
    running = True

    mob = Slime_Mob()  # skeleton_mob 객체 생성
    world.append(mob)  # 월드에 추가

# 게임 로직
def update_world():
    for game_object in world:
        game_object.update()


def render_world():
    # 월드에 객체들을 그린다.
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()

reset_world()

while running:
    update_world()
    render_world()

close_canvas()