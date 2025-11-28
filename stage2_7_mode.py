from pico2d import *

import random
import game_world
import game_framework
import stage2_8_mode
from stage2_7 import Stage2_7
from stage2_8 import Stage2_8
from player import Player
from zombie_boss import Zombie_Boss
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
            if 990 <= player.x <= 1010 and 270 <= player.y <= 370:  # 우측 문
                if not Stage2_8.stage2_8_create:
                    game_framework.push_mode(stage2_8_mode,(50, 320))
                else:
                    game_framework.pop_mode(stage2_8_mode,(50, 320))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world, zombie_boss, coins
    global stage2_7
    global player

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage2_7 = Stage2_7()

    if not Stage2_7.stage2_7_create:
        Stage2_7.stage2_7_create = True
        Stage2_7.current_mode = True

        zombie_boss = Zombie_Boss()
        zombie_boss.move_validator = stage2_7.is_mob_walkable

        coins = []
    else:
        zombie_boss = []
        coins = []

    game_world.add_object(stage2_7, 0)

    player = Player()
    player.move_validator = stage2_7.is_walkable
    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(player, 2)

    game_world.add_collision_pair('player:coin', player, None)

    # 첫 방문 시에만 몹 추가
    if zombie_boss:
        game_world.add_object(zombie_boss, 2)
        game_world.add_collision_pair('player:zombie_boss', player, None)
        game_world.add_collision_pair('player:zombie_boss', None, zombie_boss)

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
    global zombie_boss, stage2_7, coins

    Stage2_7.current_mode = False

    # 기존 zombie_mobs 초기화 후 현재 살아있는 몹만 저장
    stage2_7.saved_mobs = []
    if zombie_boss is not None and zombie_boss.is_alive:
            stage2_7.saved_mobs.append({
                'x': zombie_boss.x,
                'y': zombie_boss.y,
                'hp': zombie_boss.hp,
                'face_dir': zombie_boss.face_dir,
            })

    # 코인 저장
    stage2_7.saved_coins = []
    for coin in coins:
        stage2_7.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved {len(stage2_7.saved_mobs)} zombie mobs, {len(stage2_7.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()


def resume(player_start_pos=None):
    global zombie_boss, stage2_7, player, coins

    Stage2_7.current_mode = True

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(stage2_7, 0)
    game_world.add_object(player, 2)

    # 저장된 몹 복원
    if stage2_7.saved_mobs:
        mob_data = stage2_7.saved_mobs[0]
        zombie_boss = Zombie_Boss()
        zombie_boss.x = mob_data['x']
        zombie_boss.y = mob_data['y']
        zombie_boss.hp = mob_data['hp']
        zombie_boss.face_dir = mob_data.get('face_dir', 0)
        zombie_boss.move_validator = stage2_7.is_mob_walkable

        game_world.add_objects(zombie_boss, 2)
        game_world.add_collision_pair('player:zombie_boss', player, None)
        game_world.add_collision_pair('player:zombie_boss', None, zombie_boss)
    else:
        zombie_boss = None
        print("Resume: No saved mobs to restore")

    # 코인 복원
    if stage2_7.saved_coins:
        coins = []
        for coin_data in stage2_7.saved_coins:
            from coin import Coin
            coin = Coin()
            coin.x = coin_data['x']
            coin.y = coin_data['y']
            coin.frame = coin_data['frame']
            coins.append(coin)

        game_world.add_objects(coins, 2)
        game_world.add_collision_pair('player:coin', player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

        print(f"Resume: Restored {len(coins)} coins")

    ui = Ui()
    game_world.add_object(ui, 4)