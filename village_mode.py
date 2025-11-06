from pico2d import *

import dungeonmain_mode
import game_world
import game_framework
import title_mode
from village import Village
from village_back_object import Village_Back_Object
from village_front_object import Village_Front_Object
from player import Player


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if player.x >= 480 and player.x <=  590 and player.y >= 370 and player.y <= 380: # 던전 입구 좌표 범위
                game_framework.change_mode(dungeonmain_mode)
        else:
            player.handle_event(event)

def init():
    global world
    global village
    global player
    global back_object
    global front_object

    village = Village()
    game_world.add_object((village), 0)

    back_object = Village_Back_Object()
    game_world.add_object((back_object), 1)

    player = Player()
    # 마을 모드에서 이동 검사 콜백을 마을 객체에 위임
    player.move_validator = village.is_walkable
    game_world.add_object((player), 2)

    front_object = Village_Front_Object()
    game_world.add_object((front_object), 3)

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
