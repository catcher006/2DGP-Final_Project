import game_framework
from pico2d import *

import title_mode

image = None
logo_start_time = 0.0

def init():
    global image, running, logo_start_time

    image = load_image('logo_credit.png')
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    # Logo 모드가 2초 동안 지속되도록 설정
    global logo_start_time

    if get_time() - logo_start_time > 2.0:
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 1024, 576)
    update_canvas()

def handle_events():
    # 없는데도 받는 이유는 받지 않으면 쌓여서 queue overflow 발생
    # flush input
    events = get_events()

def pause():
    pass

def resume():
    pass