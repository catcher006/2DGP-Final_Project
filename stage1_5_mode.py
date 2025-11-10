from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
import stage1_2_mode, stage1_4_mode
from stage1_5 import Stage1_5
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
                game_framework.change_mode(stage1_2_mode)
            elif 50 <= player.x <= 70 and 270 <= player.y <= 370:  # 좌측 문
                game_framework.change_mode(stage1_4_mode)
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world
    global stage1_5
    global player
    global back_object
    global front_object

    stage1_5 = Stage1_5()
    game_world.add_object(stage1_5, 0)

    # back_object = Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    player.move_validator = stage1_5.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        player.x, player.y = player_start_pos
    else:
        player.x, player.y = 535, 60  # 기본 좌표

    game_world.add_object((player), 2)

    slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
    for slime_mob in slime_mobs:
        slime_mob.move_validator = stage1_5.is_mob_walkable
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