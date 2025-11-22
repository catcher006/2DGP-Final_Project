from pico2d import *

import random
import dungeonmain_mode
import game_world
import game_framework
#import stage2_1_mode
from stage2_0 import Stage2_0
from stage2_1 import Stage2_1
from stage2_2 import Stage2_2
from stage2_3 import Stage2_3
from stage2_4 import Stage2_4
from stage2_5 import Stage2_5
from stage2_6 import Stage2_6
from stage2_7 import Stage2_7
from stage2_8 import Stage2_8
from stage2_9 import Stage2_9
from stage2_10 import Stage2_10
from stage2_11 import Stage2_11
from player import Player
from zombie_mob import Zombie_Mob
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
            if 500 <= player.x <=  550 and 580 <= player.y <= 600: # 상단 문 (메인 던전으로 가는 문)
                if Stage2_7.boss_cleared:
                    Stage2_0.current_mode = False
                    Stage2_0.stage2_0_create = False
                    Stage2_1.stage2_1_create = False
                    Stage2_2.stage2_2_create = False
                    Stage2_3.stage2_3_create = False
                    Stage2_4.stage2_4_create = False
                    Stage2_5.stage2_5_create = False
                    Stage2_6.stage2_6_create = False
                    Stage2_7.stage2_7_create = False
                    Stage2_8.stage2_8_create = False
                    Stage2_9.stage2_9_create = False
                    Stage2_10.stage2_10_create = False
                    Stage2_11.stage2_11_create = False
                    Stage2_7.boss_cleared = False
                    game_framework.clear_stage1_modes((240, 400))

                game_framework.pop_mode(dungeonmain_mode,(240, 400))
            elif 990 <= player.x <=  1010 and 270 <= player.y <= 370: # 우측 문
                if not Stage2_1.stage2_1_create:
                    game_framework.push_mode(stage2_1_mode,(50, 320))
                else:
                    game_framework.pop_mode(stage2_1_mode,(50, 320))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world, zombie_mobs, coins
    global stage2_0
    global player

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage2_0 = Stage2_0()

    if not Stage2_0.stage2_0_create:
        Stage2_0.stage2_0_create = True
        Stage2_0.current_mode = True

        zombie_mobs = [Zombie_Mob() for _ in range(random.randint(0, 2))]
        for zombie_mob in zombie_mobs:
            zombie_mob.move_validator = stage2_0.is_mob_walkable

        coins = []
    else:
        zombie_mobs = []
        coins = []

    game_world.add_object(stage2_0, 0)

    player = Player()
    player.move_validator = stage2_0.is_walkable
    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(player, 2)

    game_world.add_collision_pair('player:coin', player, None)

    # 첫 방문 시에만 몹 추가
    if zombie_mobs:
        game_world.add_objects(zombie_mobs, 2)
        game_world.add_collision_pair('player:zombie_mob', player, None)
        for zombie_mob in zombie_mobs:
            game_world.add_collision_pair('player:zombie_mob', None, zombie_mob)
            game_world.add_collision_pair('slime_mob:zombie_mob', zombie_mob, None)

            # 다른 몹들과의 충돌 페어 추가
            for zombie_mob in zombie_mobs:
                for other_mob in zombie_mobs:
                    if zombie_mob != other_mob:
                        game_world.add_collision_pair('zombie_mob:zombie_mob', None, other_mob)

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
    global zombie_mobs, stage2_0, coins

    Stage2_0.current_mode = False

    # 기존 zombie_mobs 초기화 후 현재 살아있는 몹만 저장
    stage2_0.saved_mobs = []
    for zombie_mob in zombie_mobs:
        if zombie_mob.is_alive:
            stage2_0.saved_mobs.append({
                'type': zombie_mob.mob_type,
                'x': zombie_mob.x,
                'y': zombie_mob.y,
                'hp': zombie_mob.hp,
                'frame': zombie_mob.frame
            })

    # 코인 저장
    stage2_0.saved_coins = []
    for coin in coins:
        stage2_0.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved {len(stage2_0.saved_mobs)} zombie mobs, {len(stage2_0.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()


def resume(player_start_pos=None):
    global zombie_mobs, stage2_0, player, coins

    Stage2_0.current_mode = True

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(stage2_0, 0)
    game_world.add_object(player, 2)

    # stage2_0 인스턴스에 저장된 몹 복원
    if stage2_0.saved_mobs:
        zombie_mobs = []
        for mob_data in stage2_0.saved_mobs:
            zombie_mob = Zombie_Mob()
            zombie_mob.mob_type = mob_data['type']
            zombie_mob.x = mob_data['x']
            zombie_mob.y = mob_data['y']
            zombie_mob.hp = mob_data['hp']
            zombie_mob.frame = mob_data['frame']
            zombie_mob.move_validator = stage2_0.is_mob_walkable

            zombie_mob.move_image = load_image("./image/mobs/zombie/" + zombie_mob.mob_type + "/walk.png")
            if zombie_mob.mob_type == 'mace': zombie_mob.idle_image = load_image("./image/mobs/zombie/" + zombie_mob.mob_type + "/idle.png")
            zombie_mob.dead_image = load_image("./image/mobs/zombie/" + zombie_mob.mob_type + "/dead.png")

            zombie_mobs.append(zombie_mob)

        game_world.add_objects(zombie_mobs, 2)
        game_world.add_collision_pair('player:zombie_mob', player, None)
        for zombie_mob in zombie_mobs:
            game_world.add_collision_pair('player:zombie_mob', None, zombie_mob)
            game_world.add_collision_pair('zombie_mob:zombie_mob', zombie_mob, None)

        for zombie_mob in zombie_mobs:
            for other_mob in zombie_mobs:
                if zombie_mob != other_mob:
                    game_world.add_collision_pair('zombie_mob:zombie_mob', None, other_mob)

        print(f"Resume: Restored {len(zombie_mobs)} zombie mobs")
    else:
        print("Resume: No saved mobs to restore")

    # 코인 복원
    if stage2_0.saved_coins:
        coins = []
        for coin_data in stage2_0.saved_coins:
            coin = Coin()
            coin.x = coin_data['x']
            coin.y = coin_data['y']
            coin.frame = coin_data['frame']
            coins.append(coin)

        game_world.add_objects(coins, 2)

        game_world.add_collision_pair('player:coin', player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

        print(f"Resume: Restored {len(zombie_mobs)} slime mobs, {len(coins)} coins")
    else:
        print(f"Resume: Restored {len(zombie_mobs)} slime mobs, 0 coins")

    ui = Ui()
    game_world.add_object(ui, 4)