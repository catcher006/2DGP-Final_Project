from pico2d import *

import dungeonmain_mode
import game_world
import game_framework
import title_mode
from village import Village
from village_front_object import Village_Front_Object
from player import Player
from ui import Ui


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if 480 <= player.x <= 590 and 370 <= player.y <= 380: # 던전 입구 좌표 범위
                game_framework.push_mode(dungeonmain_mode,(535, 60))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world
    global village
    global player
    global back_object
    global front_object

    village = Village()
    game_world.add_object((village), 0)

    # back_object = Village_Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    # 마을 모드에서 이동 검사 콜백을 마을 객체에 위임
    player.move_validator = village.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        player.x, player.y = player_start_pos
    else:
        player.x, player.y = 510, 160  # 기본 좌표
    game_world.add_object((player), 2)

    front_object = Village_Front_Object()
    game_world.add_object((front_object), 3)

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
    # 충돌 페어도 정리
    game_world.collision_pairs.clear()

def resume(player_start_pos=None):
    # 필요시 village 객체들을 다시 초기화
    global village, back_object, front_object, player

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(village, 0)
    game_world.add_object(player, 2)
    game_world.add_object(front_object, 3)

    ui = Ui()
    game_world.add_object(ui, 4)
