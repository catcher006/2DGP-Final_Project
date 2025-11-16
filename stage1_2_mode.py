from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
import stage1_1_mode
import stage1_5_mode
import stage1_manger
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
            # 모드 전환 전에 현재 상태 저장
            if len(slime_mobs) >= 1:
                stage1_manger.stage1_0_last_mob1_pos = (slime_mobs[0].x, slime_mobs[0].y)
            if len(slime_mobs) >= 2:
                stage1_manger.stage1_0_last_mob2_pos = (slime_mobs[1].x, slime_mobs[1].y)

            # 모든 슬라임의 상태를 리스트로 저장
            mobs_state = []
            for slime in slime_mobs:
                state = {
                    'type': getattr(slime, 'mob_type', None),
                    'x': getattr(slime, 'x', None),
                    'y': getattr(slime, 'y', None),
                    'frame': getattr(slime, 'frame', 0),
                    'is_move': getattr(slime, 'is_move', True),
                    'lr_dir': getattr(slime, 'lr_dir', 0),
                    'ud_dir': getattr(slime, 'ud_dir', 0),
                    'hp': getattr(slime, 'hp', 100),
                    'is_alive': getattr(slime, 'is_alive', True)
                }
                mobs_state.append(state)
            stage1_manger.stage1_2_mobs = mobs_state

            if 500 <= player.x <=  550 and 0 <= player.y <= 20: # 하단 문
                game_framework.change_mode(stage1_5_mode, (525, 600))
            elif 50 <= player.x <=  70 and 270 <= player.y <= 370: # 좌측 문
                game_framework.change_mode(stage1_1_mode, (1010, 320))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world, slime_mobs
    global stage1_2
    global player
    global back_object
    global front_object

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage1_2 = Stage1_2()
    game_world.add_object(stage1_2, 0)

    # back_object = Back_Object()
    # game_world.add_object((back_object), 1)

    player = Player()
    player.move_validator = stage1_2.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        player.x, player.y = player_start_pos
    else:
        player.x, player.y = 535, 60  # 기본 좌표

    game_world.add_object((player), 2)

    slime_mobs = []
    if not stage1_manger.stage1_2_create:
        slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
        for slime_mob in slime_mobs:
            slime_mob.move_validator = stage1_2.is_mob_walkable
        # 슬라임이 0개여도 생성 완료로 표시
        stage1_manger.stage1_2_create = True

        # 초기 상태를 빈 리스트로 저장 (0개인 경우 대비)
        if not slime_mobs:
            stage1_manger.stage1_2_mobs = []
    else:
        # 저장된 상태에서 복원
        saved_mobs = stage1_manger.stage1_2_mobs  # 함수가 아닌 변수 직접 사용
        if saved_mobs:
            for mob_state in saved_mobs:
                # dict에서 Slime_Mob 객체로 복원
                slime = Slime_Mob()
                if mob_state.get('type'):
                    slime.mob_type = mob_state['type']
                    slime.move_image = load_image(f"./image/mobs/slime/{slime.mob_type}_Slime_Jump.png")
                    slime.idle_image = load_image(f"./image/mobs/slime/{slime.mob_type}_Slime_Jump.png")
                    slime.dead_image = load_image(f"./image/mobs/slime/{slime.mob_type}_Slime_Dead.png")
                slime.x = mob_state.get('x', slime.x)
                slime.y = mob_state.get('y', slime.y)
                slime.frame = mob_state.get('frame', slime.frame)
                slime.is_move = mob_state.get('is_move', slime.is_move)
                slime.lr_dir = mob_state.get('lr_dir', slime.lr_dir)
                slime.ud_dir = mob_state.get('ud_dir', slime.ud_dir)
                slime.hp = mob_state.get('hp', slime.hp)
                slime.is_alive = mob_state.get('is_alive', slime.is_alive)
                slime.move_validator = stage1_2.is_mob_walkable
                slime_mobs.append(slime)

    game_world.add_objects(slime_mobs, 2)

    game_world.add_collision_pair('player:slime_mob', player, None)
    for slime_mob in slime_mobs:
        game_world.add_collision_pair('player:slime_mob', None, slime_mob)


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
    pass

def resume():
    pass