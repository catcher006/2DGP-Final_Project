from pico2d import *

import random
import game_world
import game_framework
import stage1_1_mode
import stage1_5_mode
from stage1_2 import Stage1_2
from stage1_1 import Stage1_1
from stage1_5 import Stage1_5
from player import Player
from slime_mob import Slime_Mob
from coin import Coin
from ui import Ui


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
            if 500 <= player.x <=  550 and 0 <= player.y <= 20: # 하단 문
                if not Stage1_5.stage1_5_create:
                    game_framework.push_mode(stage1_5_mode, (525, 600))
                else:
                    game_framework.pop_mode(stage1_5_mode, (525, 600))
            elif 50 <= player.x <=  70 and 270 <= player.y <= 370: # 좌측 문
                if not Stage1_1.stage1_1_create:
                    game_framework.push_mode(stage1_1_mode, (1010, 320))
                else:
                    game_framework.pop_mode(stage1_1_mode, (1010, 320))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world, slime_mobs, coins
    global stage1_2
    global player

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage1_2 = Stage1_2()

    if not Stage1_2.stage1_2_create:
        Stage1_2.stage1_2_create = True
        Stage1_2.current_mode = True

        slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
        for slime_mob in slime_mobs:
            slime_mob.move_validator = stage1_2.is_mob_walkable

        coins = []
    else:
        slime_mobs = []
        coins = []

    game_world.add_object(stage1_2, 0)

    player = Player()
    player.move_validator = stage1_2.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object((player), 2)

    game_world.add_collision_pair('player:coin', player, None)

    # 첫 방문 시에만 몹 추가
    if slime_mobs:
        game_world.add_objects(slime_mobs, 2)
        game_world.add_collision_pair('player:slime_mob', player, None)
        for slime_mob in slime_mobs:
            game_world.add_collision_pair('player:slime_mob', None, slime_mob)
            game_world.add_collision_pair('slime_mob:slime_mob', slime_mob, None)

        # 다른 몹들과의 충돌 페어 추가
        for slime_mob in slime_mobs:
            for other_mob in slime_mobs:
                if slime_mob != other_mob:
                    game_world.add_collision_pair('slime_mob:slime_mob', None, other_mob)

    if coins:
        game_world.add_objects(coins, 2)
        game_world.add_collision_pair('player:coin', player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

    ui = Ui()
    game_world.add_object(ui, 4)

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
    global slime_mobs, stage1_2, coins

    Stage1_2.current_mode = False

    # 기존 saved_mobs 초기화 후 현재 살아있는 몹만 저장
    stage1_2.saved_mobs = []
    for slime_mob in slime_mobs:
        if slime_mob.is_alive:
            stage1_2.saved_mobs.append({
                'type': slime_mob.mob_type,
                'x': slime_mob.x,
                'y': slime_mob.y,
                'hp': slime_mob.hp,
                'frame': slime_mob.frame
            })

    # 코인 저장
    stage1_2.saved_coins = []
    for coin in coins:
        stage1_2.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved {len(stage1_2.saved_mobs)} slime mobs, {len(stage1_2.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()


def resume(player_start_pos=None):
    global slime_mobs, stage1_2, player, coins

    Stage1_2.current_mode = True

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(stage1_2, 0)
    game_world.add_object(player, 2)

    # stage1_2 인스턴스에 저장된 몹 복원
    if stage1_2.saved_mobs:
        slime_mobs = []
        for mob_data in stage1_2.saved_mobs:
            slime_mob = Slime_Mob()
            slime_mob.mob_type = mob_data['type']
            slime_mob.x = mob_data['x']
            slime_mob.y = mob_data['y']
            slime_mob.hp = mob_data['hp']
            slime_mob.frame = mob_data['frame']
            slime_mob.move_validator = stage1_2.is_mob_walkable

            slime_mob.move_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.idle_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.dead_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Dead.png")

            slime_mobs.append(slime_mob)

        game_world.add_objects(slime_mobs, 2)
        game_world.add_collision_pair('player:slime_mob', player, None)
        for slime_mob in slime_mobs:
            game_world.add_collision_pair('player:slime_mob', None, slime_mob)
            game_world.add_collision_pair('slime_mob:slime_mob', slime_mob, None)

        for slime_mob in slime_mobs:
            for other_mob in slime_mobs:
                if slime_mob != other_mob:
                    game_world.add_collision_pair('slime_mob:slime_mob', None, other_mob)

        print(f"Resume: Restored {len(slime_mobs)} slime mobs")
    else:
        print("Resume: No saved mobs to restore")

    # 코인 복원
    if stage1_2.saved_coins:
        coins = []
        for coin_data in stage1_2.saved_coins:
            coin = Coin()
            coin.x = coin_data['x']
            coin.y = coin_data['y']
            coin.frame = coin_data['frame']
            coins.append(coin)

        game_world.add_objects(coins, 2)

        game_world.add_collision_pair('player:coin', player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

        print(f"Resume: Restored {len(slime_mobs)} slime mobs, {len(coins)} coins")
    else:
        print(f"Resume: Restored {len(slime_mobs)} slime mobs, 0 coins")

    ui = Ui()
    game_world.add_object(ui, 4)