from pico2d import *
from state_machine import StateMachine
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f

class Move:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        self.player.image.clip_draw(int(self.player.frame) * 128, 128 * self.player.face_dir, 128, 128, self.player.x, self.player.y, 200, 200)

class Player:
    def __init__(self):
        self.image = load_image("sword_attack.png")  # 플레이어 이미지 로드

        self.x = 400
        self.y = 300

        self.frame = 12
        self.face_dir = 3
        self.is_move = True

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0  # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0  # left right direction (left: -1, right: 1, none: 0)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.hp = 100  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

        self.MOVE = Move(self)

        self.state_machine = StateMachine(
            self.MOVE,
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
        # return self.x - 68, self.y - 10, self.x - 40, self.y + 8  # frame : 0
        # return self.x - 68, self.y - 48, self.x + 30, self.y + 8  # frame : 1
        # return self.x + 12, self.y - 48, self.x + 83, self.y - 6  # frame : 2
        # return self.x - 25, self.y - 42, self.x + 83, self.y - 6  # frame : 3
        # return self.x - 25, self.y - 28, self.x + 50, self.y - 6  # frame : 4
        # return self.x - 25, self.y - 28, self.x + 25, self.y - 8  # frame : 5
        # return self.x + 15, self.y - 28, self.x + 38, self.y - 10  # frame : 6
        # return self.x - 30, self.y - 23, self.x + 15, self.y - 17  # frame : 7
        # return self.x - 30, self.y - 23, self.x + 35, self.y - 4  # frame : 8
        # return self.x + 5, self.y - 48, self.x + 83, self.y - 6  # frame : 9
        # return self.x - 52, self.y - 50, self.x + 55, self.y - 20  # frame : 10
        # return self.x - 52, self.y - 52, self.x + 25, self.y - 15  # frame : 11
        # return self.x - 52, self.y - 34, self.x - 22, self.y - 12  # frame : 12

        # face_dir = 1
        # return self.x - 28, self.y + 5, self.x - 20, self.y + 42  # frame : 0
        # return self.x - 56, self.y - 23, self.x - 20, self.y + 36  # frame : 1
        # return self.x - 56, self.y - 48, self.x + 52, self.y - 18  # frame : 2
        # return self.x - 12, self.y - 48, self.x + 52, self.y - 8  # frame : 3
        # return self.x + 12, self.y - 34, self.x + 54, self.y - 8  # frame : 4
        # return self.x + 12, self.y - 25, self.x + 24, self.y - 10  # frame : 5
        # return self.x - 20, self.y - 30, self.x + 18, self.y - 14  # frame : 6
        # return self.x + 8, self.y - 30, self.x + 22, self.y - 12  # frame : 7
        # return self.x + 8, self.y - 40, self.x + 56, self.y - 12  # frame : 8
        # return self.x - 68, self.y - 56, self.x + 56, self.y - 12  # frame : 9
        # return self.x - 76, self.y - 56, self.x, self.y + 4  # frame : 10
        # return self.x - 76, self.y - 50, self.x - 30, self.y + 4  # frame : 11
        # return self.x - 74, self.y - 10, self.x - 30, self.y + 4  # frame : 12

        # face_dir = 2
        # return self.x + 34, self.y - 10, self.x + 66, self.y + 8  # frame : 0
        # return self.x - 30, self.y - 46, self.x + 66, self.y + 8  # frame : 1
        # return self.x - 84, self.y - 48, self.x - 16, self.y - 6  # frame : 2
        # return self.x - 84, self.y - 42, self.x + 24, self.y - 6  # frame : 3
        # return self.x - 54, self.y - 28, self.x + 24, self.y - 6  # frame : 4
        # return self.x - 26, self.y - 28, self.x + 24, self.y - 10  # frame : 5
        # return self.x - 38, self.y - 28, self.x - 8, self.y - 10  # frame : 6
        # return self.x - 8, self.y - 22, self.x + 30, self.y - 18  # frame : 7
        # return self.x - 36, self.y - 22, self.x + 30, self.y - 6  # frame : 8
        # return self.x - 84, self.y - 48, self.x - 8, self.y - 6  # frame : 9
        # return self.x - 58, self.y - 52, self.x + 52, self.y - 18  # frame : 10
        # return self.x - 16, self.y - 52, self.x + 52, self.y - 18  # frame : 11
        # return self.x + 26, self.y - 32, self.x + 52, self.y - 18  # frame : 12

        # face_dir = 3
        # return self.x + 14, self.y - 44, self.x + 32, self.y - 26  # frame : 0
        # return self.x + 24, self.y - 44, self.x + 60, self.y - 4  # frame : 1
        # return self.x - 44, self.y - 20, self.x + 60, self.y + 14  # frame : 2
        # return self.x - 48, self.y - 40, self.x, self.y + 14  # frame : 3
        # return self.x - 50, self.y - 40, self.x, self.y + 14  # frame : 4
        # return self.x - 38, self.y - 40, self.x - 20, self.y - 20  # frame : 5
        # return self.x - 24, self.y - 30, self.x + 24, self.y - 4  # frame : 6
        # return self.x - 22, self.y - 48, self.x - 16, self.y - 24  # frame : 7
        # return self.x - 52, self.y - 46, self.x - 22, self.y - 4  # frame : 8
        # return self.x - 48, self.y - 6, self.x + 44, self.y + 18  # frame : 9
        # return self.x - 28, self.y - 14, self.x + 78, self.y + 18  # frame : 10
        # return self.x + 32, self.y - 14, self.x + 78, self.y + 12  # frame : 11
        return self.x + 32, self.y - 14, self.x + 78, self.y - 8  # frame : 12

open_canvas(1200,800)

def reset_world():
    global running
    global world # World List - 모든 객체를 갖고 있는 리스트
    global player

    world = [] # 하나도 객체가 없는 월드
    running = True

    player = Player()  # skeleton_mob 객체 생성
    world.append(player)  # 월드에 추가

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