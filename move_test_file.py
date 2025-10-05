from pico2d import *
import random

class Boy:
    def __init__(self):
        self.image = load_image('skeleton_none_walk_all.png')
        self.x = random.randint(0, 700)
        self.y = 90
        self.frame = random.randint(0, 7)

    def draw(self):
        self.image.clip_draw(self.frame * 64, 64*0, 64, 64, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 8

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

def handle_events():
    global running
    global boy  # 제어할 소년 객체
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_w:
                boy.move(0, 10)
            elif event.key == SDLK_s:
                boy.move(0, -10)
            elif event.key == SDLK_a:
                boy.move(-10, 0)
            elif event.key == SDLK_d:
                boy.move(10, 0)

open_canvas(1200,800)

def reset_world():
    global running
    global world # World List - 모든 객체를 갖고 있는 리스트
    global boy

    world = [] # 하나도 객체가 없는 월드
    running = True

    boy = Boy()  # Boy 객체 생성
    world.append(boy)  # 월드에 추가

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
    handle_events()
    update_world()
    render_world()
    delay(0.1)

close_canvas()
