from pico2d import *

import game_world
import game_framework
import title_mode
from BackGround import Background
from Back_Object import Back_Object
from Front_object import Front_Object
from Player import Player


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)

def init():
    global world
    global background
    global player
    global back_object
    global front_object

    background = Background()
    game_world.add_object((background), 0)

    back_object = Back_Object()
    game_world.add_object((back_object), 1)

    player = Player()
    game_world.add_object((player), 2)

    front_object = Front_Object()
    game_world.add_object((front_object), 3)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass
