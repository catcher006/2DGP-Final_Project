from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
import stage1_1_mode
import stage1_3_mode
import stage1_manger
from player_sword import Player_Sword
from stage1_0 import Stage1_0
from player import Player
from slime_mob import Slime_Mob


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        # 마우스 이벤트는 무시
        elif event.type in (SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            continue
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
            if 500 <= player.x <=  550 and 580 <= player.y <= 600: # 상단 문 (메인 던전으로 가는 문)
                game_framework.pop_mode(dungeonmain_mode,(240, 400))
            elif 990 <= player.x <=  1010 and 270 <= player.y <= 370: # 우측 문
                game_framework.change_mode(stage1_1_mode,(50, 320))
            elif 500 <= player.x <=  550 and 0 <= player.y <= 20: # 하단 문
                game_framework.change_mode(stage1_3_mode,(525, 600))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world, slime_mobs
    global stage1_0
    global player
    global back_object
    global front_object

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage1_0 = Stage1_0()
    game_world.add_object(stage1_0, 0)

    # back_object = Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    player.move_validator = stage1_0.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object((player), 2)

    # 첫 방문인 경우만 새로 생성
    if stage1_manger.stage1_0_create is None:
        slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
        for slime_mob in slime_mobs:
            slime_mob.move_validator = stage1_0.is_mob_walkable
        stage1_manger.stage1_0_create = True

        game_world.add_objects(slime_mobs, 2)
        game_world.add_collision_pair('player:slime_mob', player, None)
        for slime_mob in slime_mobs:
            game_world.add_collision_pair('player:slime_mob', None, slime_mob)
    else:
        # 재방문인 경우 빈 리스트로 초기화 (resume에서 복원)
        slime_mobs = []


    # front_object = Front_Object()
    # game_world.add_object((front_object), 3)

def update():
    game_world.update()
    game_world.handle_collsions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    """push_mode로 나갈 때 현재 상태 저장 및 게임 월드 정리"""
    global slime_mobs

    # 현재 살아있는 slime_mob들의 상태를 저장
    alive_mobs = []
    for slime_mob in slime_mobs:
        if slime_mob.is_alive:
            mob_data = {
                'type': slime_mob.mob_type,
                'x': slime_mob.x,
                'y': slime_mob.y,
                'hp': slime_mob.hp,
                'frame': slime_mob.frame
            }
            alive_mobs.append(mob_data)

    # 상태 저장
    stage1_manger.stage1_0_mobs = alive_mobs
    print(f"Pause: Saved {len(alive_mobs)} slime mobs")

    # 월드와 충돌 페어를 완전히 정리해서 다른 모드로 갔을 때 잔존 오브젝트가 없게 함
    game_world.clear()
    game_world.collision_pairs.clear()


def resume(player_start_pos=None):
    """pop_mode로 돌아올 때 저장된 상태 복원"""
    global slime_mobs, stage1_0, player

    if player_start_pos:
        player.x, player.y = player_start_pos

    # 배경과 플레이어 다시 추가 (player 객체는 모듈 변수로 유지됨)
    game_world.add_object(stage1_0, 0)
    game_world.add_object(player, 2)

    # 저장된 몹 데이터가 있으면 복원
    if stage1_manger.stage1_0_mobs is not None:
        slime_mobs = []

        for mob_data in stage1_manger.stage1_0_mobs:
            slime_mob = Slime_Mob()
            slime_mob.mob_type = mob_data['type']
            slime_mob.x = mob_data['x']
            slime_mob.y = mob_data['y']
            slime_mob.hp = mob_data['hp']
            slime_mob.frame = mob_data['frame']
            slime_mob.move_validator = stage1_0.is_mob_walkable

            # 이미지 다시 로드
            slime_mob.move_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.idle_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.dead_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Dead.png")

            slime_mobs.append(slime_mob)

        # 게임 월드에 추가
        game_world.add_objects(slime_mobs, 2)

        # 충돌 페어 재설정
        game_world.add_collision_pair('player:slime_mob', player, None)
        for slime_mob in slime_mobs:
            game_world.add_collision_pair('player:slime_mob', None, slime_mob)

        print(f"Resume: Restored {len(slime_mobs)} slime mobs")
    else:
        print("Resume: No saved mobs to restore")