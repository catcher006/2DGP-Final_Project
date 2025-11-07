from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
import stage1_4_mode
import stage1_6_mode
from stage1_7 import Stage1_7
from player import Player
from slime_mob import Slime_Mob


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if 500 <= player.x <=  550 and 580 <= player.y <= 600: # 상단 문
                game_framework.change_mode(stage1_4_mode)
            elif 0 <= player.x <=  20 and 270 <= player.y <= 370: # 좌측 문
                game_framework.change_mode(stage1_6_mode)
        else:
            player.handle_event(event)

def init():
    global world
    global stage1_7
    global player
    global back_object
    global front_object

    stage1_7 = Stage1_7()
    game_world.add_object(stage1_7, 0)

    # back_object = Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    player.move_validator = stage1_7.is_walkable
    player.x = 535
    player.y = 540

    game_world.add_object((player), 2)

    slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
    for slime_mob in slime_mobs:
        slime_mob.move_validator = stage1_7.is_mob_walkable
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