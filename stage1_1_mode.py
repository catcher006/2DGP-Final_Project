from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
import stage1_0_mode, stage1_2_mode
from stage1_1 import Stage1_1
from player import Player
from slime_mob import Slime_Mob

stage1_1 = None
player = None
slime_mobs = []
_initialized = False


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if 990 <= player.x <=  1100 and 270 <= player.y <= 370: # 우측 문
                game_framework.change_mode(stage1_2_mode)
            elif 0 <= player.x <=  20 and 270 <= player.y <= 370: # 좌측 문
                game_framework.change_mode(stage1_0_mode)
        else:
            player.handle_event(event)

def init():
    global world
    global stage1_1
    global player
    global back_object
    global front_object
    global slime_mobs
    global _initialized

    if not _initialized:
        stage1_1 = Stage1_1()
        game_world.add_object(stage1_1, 0)

        # back_object = Back_Object()
        # game_world.add_object((back_object), 1)

        player = Player()
        player.move_validator = stage1_1.is_walkable
        player.x = 535
        player.y = 540

        game_world.add_object((player), 2)

        slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
        for slime_mob in slime_mobs:
            slime_mob.move_validator = stage1_1.is_mob_walkable
        game_world.add_objects(slime_mobs, 2)

        # front_object = Front_Object()
        # game_world.add_object((front_object), 3)

        _initialized = True
    else:
        resume()

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    global stage1_1, player, slime_mobs, _initialized
    try:
        if stage1_1: game_world.remove_object(stage1_1)
    except:
        pass
    try:
        if player: game_world.remove_object(player)
    except:
        pass
    for m in list(slime_mobs):
        try:
            game_world.remove_object(m)
        except:
            pass
    stage1_1 = None
    player = None
    slime_mobs = []
    _initialized = False

def pause():
    try:
        if stage1_1: game_world.remove_object(stage1_1)
    except:
        pass
    try:
        if player: game_world.remove_object(player)
    except:
        pass
    for m in list(slime_mobs):
        try:
            game_world.remove_object(m)
        except:
            pass

def resume():
    if stage1_1:
        game_world.add_object(stage1_1, 0)
    if player:
        game_world.add_object(player, 2)
    if slime_mobs:
        game_world.add_objects(slime_mobs, 2)