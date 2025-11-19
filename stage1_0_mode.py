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

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    # Stage1_0 인스턴스는 항상 존재하도록 보장
    if 'stage1_0' not in globals() or stage1_0 is None:
        stage1_0 = Stage1_0()

    # 첫 방문 시에만 stage1_0 인스턴스 생성
    if not stage1_0.is_created:
        stage1_0 = Stage1_0()
        stage1_0.is_created = True

        slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
        for slime_mob in slime_mobs:
            slime_mob.move_validator = stage1_0.is_mob_walkable
    else:
        slime_mobs = []

    game_world.add_object(stage1_0, 0)

    player = Player()
    player.move_validator = stage1_0.is_walkable
    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(player, 2)

    # 첫 방문 시에만 몹 추가
    if slime_mobs:
        game_world.add_objects(slime_mobs, 2)
        game_world.add_collision_pair('player:slime_mob', player, None)
        for slime_mob in slime_mobs:
            game_world.add_collision_pair('player:slime_mob', None, slime_mob)

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
    global slime_mobs, stage1_0

    # 기존 saved_mobs 초기화 후 현재 살아있는 몹만 저장
    stage1_0.saved_mobs = []
    for slime_mob in slime_mobs:
        if slime_mob.is_alive:
            stage1_0.saved_mobs.append({
                'type': slime_mob.mob_type,
                'x': slime_mob.x,
                'y': slime_mob.y,
                'hp': slime_mob.hp,
                'frame': slime_mob.frame
            })

    print(f"Pause: Saved {len(stage1_0.saved_mobs)} slime mobs")

    game_world.clear()
    game_world.collision_pairs.clear()


def resume(player_start_pos=None):
    global slime_mobs, stage1_0, player

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(stage1_0, 0)
    game_world.add_object(player, 2)

    # stage1_0 인스턴스에 저장된 몹 복원
    if stage1_0.saved_mobs:
        slime_mobs = []
        for mob_data in stage1_0.saved_mobs:
            slime_mob = Slime_Mob()
            slime_mob.mob_type = mob_data['type']
            slime_mob.x = mob_data['x']
            slime_mob.y = mob_data['y']
            slime_mob.hp = mob_data['hp']
            slime_mob.frame = mob_data['frame']
            slime_mob.move_validator = stage1_0.is_mob_walkable

            slime_mob.move_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.idle_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.dead_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Dead.png")

            slime_mobs.append(slime_mob)

        game_world.add_objects(slime_mobs, 2)
        game_world.add_collision_pair('player:slime_mob', player, None)
        for slime_mob in slime_mobs:
            game_world.add_collision_pair('player:slime_mob', None, slime_mob)

        print(f"Resume: Restored {len(slime_mobs)} slime mobs")
    else:
        print("Resume: No saved mobs to restore")