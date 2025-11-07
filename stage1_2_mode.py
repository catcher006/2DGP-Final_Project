from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
import stage1_1_mode
import stage1_5_mode
from stage1_2 import Stage1_2
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
                game_framework.change_mode(dungeonmain_mode)
            elif 990 <= player.x <=  1100 and 270 <= player.y <= 370: # 우측 문
                game_framework.change_mode(dungeonmain_mode)
            elif 500 <= player.x <=  550 and 0 <= player.y <= 20: # 하단 문
                game_framework.change_mode(stage1_5_mode)
            elif 0 <= player.x <=  20 and 270 <= player.y <= 370: # 좌측 문
                game_framework.change_mode(stage1_1_mode)
        else:
            player.handle_event(event)

def init():
    global world
    global stage1_2
    global player
    global back_object
    global front_object

    stage1_2 = Stage1_2()
    game_world.add_object(stage1_2, 0)

    # back_object = Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    player.move_validator = stage1_2.is_walkable
    player.x = 535
    player.y = 540

    game_world.add_object((player), 2)

    slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
    for slime_mob in slime_mobs:
        slime_mob.move_validator = stage1_2.is_mob_walkable
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