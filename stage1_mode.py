from pico2d import *

import game_world
import game_framework
from stage1 import Stage1
from player import Player
from slime_mob import Slime_Mob


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global world
    global stage1
    global player
    global back_object
    global front_object

    stage1 = Stage1()
    game_world.add_object(stage1, 0)

    # back_object = Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    player.move_validator = stage1.is_walkable
    player.x = 535
    player.y = 540

    game_world.add_object((player), 2)

    slime_mobs = [Slime_Mob() for _ in range(5)]
    for slime_mob in slime_mobs:
        slime_mob.move_validator = stage1.is_walkable
    game_world.add_objects(slime_mobs, 2)


    # front_object = Front_Object()
    # game_world.add_object((front_object), 3)

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