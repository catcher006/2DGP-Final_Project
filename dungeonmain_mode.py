from pico2d import *

import village_mode
import stage1_0_mode
import game_world
import game_framework
from dungeonmain import Dungeonmain
from player import Player


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if player.x >= 195 and player.x <= 290 and player.y >= 380 and player.y <= 400:  # 1번 스테이지 입구 좌표 범위
                game_framework.change_mode(stage1_0_mode,(525, 600))
            elif player.x >= 505 and player.x <= 585 and player.y >= 380 and player.y <= 400:  # 2번 스테이지 입구 좌표 범위
                print("Stage 2 Entered") # 스테이지 2로 이동
            elif player.x >= 780 and player.x <= 880 and player.y >= 380 and player.y <= 400:  # 3번 스테이지 입구 좌표 범위
                print("Stage 3 Entered") # 스테이지 3로 이동
            elif player.x >= 500 and player.x <= 600 and player.y >= 60 and player.y <= 80:  # 마을 입구 좌표 범위
                game_framework.change_mode(village_mode,(535, 380))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world
    global dungeonmain
    global player
    global back_object
    global front_object

    dungeonmain = Dungeonmain()
    game_world.add_object((dungeonmain), 0)

    # back_object = Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    player.move_validator = dungeonmain.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        player.x, player.y = player_start_pos
    else:
        player.x, player.y = 535, 60  # 기본 좌표

    game_world.add_object((player), 2)

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