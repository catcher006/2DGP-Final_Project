from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
import stage1_1_mode
import stage1_3_mode
from stage1_0 import Stage1_0
from player import Player
from slime_mob import Slime_Mob

# 모드가 가지고 있을 객체들(전역으로 보존)
stage1_0 = None
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
                game_framework.change_mode(stage1_1_mode)
            elif 500 <= player.x <=  550 and 0 <= player.y <= 20: # 하단 문
                game_framework.change_mode(stage1_3_mode)
        else:
            player.handle_event(event)

def init():
    global world
    global stage1_0
    global player
    global back_object
    global front_object
    global slime_mobs
    global _initialized

    if not _initialized:
        stage1_0 = Stage1_0()
        game_world.add_object(stage1_0, 0)

        # back_object = Back_Object()
        # game_world.add_object((back_object), 1)

        player = Player()
        player.move_validator = stage1_0.is_walkable
        player.x = 535
        player.y = 540

        game_world.add_object((player), 2)

        slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
        for slime_mob in slime_mobs:
            slime_mob.move_validator = stage1_0.is_mob_walkable
        game_world.add_objects(slime_mobs, 2)

        # front_object = Front_Object()
        # game_world.add_object((front_object), 3)

        _initialized = True
    else:
        # 이미 초기화된 모드를 다시 init으로 들어오는 경우(안전 장치)
        # 기존 객체가 game_world에 없다면 resume으로 복구
        resume()

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    global stage1_0, player, slime_mobs, _initialized
    # 모드 종료 시 자신이 추가한 객체만 제거/해제
    try:
        if stage1_0: game_world.remove_object(stage1_0)
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
    # 해제
    stage1_0 = None
    player = None
    slime_mobs = []
    _initialized = False

def pause():
    # push 시 현재 모드의 객체들을 game_world에서 제거(참조는 유지)
    try:
        if stage1_0: game_world.remove_object(stage1_0)
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
    # pop 시 객체들을 다시 game_world에 추가 (재생성 없음)
    if stage1_0:
        game_world.add_object(stage1_0, 0)
    if player:
        game_world.add_object(player, 2)
    if slime_mobs:
        game_world.add_objects(slime_mobs, 2)