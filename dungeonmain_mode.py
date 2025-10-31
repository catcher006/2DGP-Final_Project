import game_framework
from pico2d import *

image = None

def init():
    global image
    image = load_image('dungeon_main.png')

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 1024, 576)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

def pause():
    pass

def resume():
    pass