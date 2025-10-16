from pico2d import *

from BackGround import Background
from Back_Object import Back_Object
from Front_object import Front_Object
from Player import Player


class Slime_Mob:
    pass

class Slime_Boss:
    pass

class Skeleton_Mob:
    pass

class Skeleton_Boss:
    pass

class Goblin_Mob:
    pass

class Goblin_Boss:
    pass


class Item:
    pass

class UI:
    pass

################################
def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

def reset_world():
    global world
    global background
    global player
    global back_object
    global front_object

    world = []

    background = Background()
    world.append(background)

    back_object = Back_Object()
    world.append(back_object)

    player = Player()
    world.append(player)

    front_object = Front_Object()
    world.append(front_object)

def update_world():
    for game_object in world:
        game_object.update()

def render_world():
    clear_canvas()

    for game_object in world:
        game_object.draw()

    update_canvas()

running = True

open_canvas(1024,576)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.07)

close_canvas()