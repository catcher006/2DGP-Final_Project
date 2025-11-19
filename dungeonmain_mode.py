from pico2d import *

import village_mode
import stage1_0_mode
import game_world
import game_framework
from dungeonmain import Dungeonmain
from player import Player
from stage1_0 import Stage1_0
from ui import Ui


def handle_events():
    global running
    global stage1_0

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        # 마우스 이벤트는 무시
        elif event.type in (SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            continue
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if 195 <= player.x <= 290 and 380 <= player.y <= 400:  # 1번 스테이지 입구 좌표 범위
                if not Stage1_0.stage1_0_create:
                    game_framework.push_mode(stage1_0_mode, (525, 600))
                else:
                    game_framework.pop_mode(stage1_0_mode, (525, 600))
            elif 505 <= player.x <= 585 and 380 <= player.y <= 400:  # 2번 스테이지 입구 좌표 범위
                print("Stage 2 Entered") # 스테이지 2로 이동
            elif 780 <= player.x <= 880 and 380 <= player.y <= 400:  # 3번 스테이지 입구 좌표 범위
                print("Stage 3 Entered") # 스테이지 3로 이동
            elif 500 <= player.x <= 600 and 60 <= player.y <= 80:  # 마을 입구 좌표 범위
                game_framework.pop_mode(village_mode,(535, 380))
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

    ui = Ui()
    game_world.add_object(ui, 4)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    # 현재 모드의 모든 객체를 게임 월드에서 제거
    game_world.clear()

def resume(player_start_pos=None):
    # 필요시 dungeonmain 객체들을 다시 초기화
    global dungeonmain, player

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(dungeonmain, 0)
    game_world.add_object(player, 2)

    ui = Ui()
    game_world.add_object(ui, 4)