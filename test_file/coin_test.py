import random

import game_framework
from state_machine import StateMachine
from pico2d import load_image, load_font, get_time, draw_rectangle, open_canvas, clear_canvas, update_canvas, \
    close_canvas

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Coin:
    def __init__(self):
        self.image = load_image("coin.png")
        self.frame = 7
        self.x, self.y = 512, 288
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass
    def draw(self):
        self.image.clip_draw(int(self.frame) * 17,0, 17, 16, self.x, self.y, 32, 32)
        draw_rectangle(*self.get_bb())
    def update(self):
        # self.frame = (int(self.frame) + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        pass

    def get_bb(self):
        # return self.x - 17, self.y - 16, self.x + 15, self.y + 15  # frame : 0
        # return self.x - 15, self.y - 16, self.x + 12, self.y + 15  # frame : 1
        # return self.x - 12, self.y - 16, self.x + 8, self.y + 15  # frame : 2
        # return self.x - 8, self.y - 16, self.x + 4, self.y + 15  # frame : 3
        # return self.x - 5, self.y - 16, self.x + 3, self.y + 15  # frame : 4
        # return self.x - 8, self.y - 16, self.x + 4, self.y + 15  # frame : 5
        # return self.x - 12, self.y - 16, self.x + 8, self.y + 15  # frame : 6
        return self.x - 15, self.y - 16, self.x + 12, self.y + 15  # frame : 7

open_canvas(1200,800)

def reset_world():
    global running
    global world # World List - 모든 객체를 갖고 있는 리스트
    global coin

    world = [] # 하나도 객체가 없는 월드
    running = True

    coin = Coin()
    world.append(coin)  # 월드에 추가

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