from pico2d import *

import random
import game_world
import game_framework
import stage1_0_mode, stage1_6_mode
import common
from stage1_3 import Stage1_3
from stage1_0 import Stage1_0
from stage1_6 import Stage1_6
from player import Player
from slime_mob import Slime_Mob
from coin import Coin
from ui import Ui


def handle_events():
    global running
    global ui

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif Ui.paused:
            if ui.handle_events(event):
                continue
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            import sounds
            sounds.normal_click_sound.play()
            mx = event.x
            my = get_canvas_height() - event.y

            if 970 <= mx <= 1010 and 530 <= my <= 570:
                Ui.paused = not Ui.paused
                continue
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
            if 500 <= common.player.x <=  550 and 580 <= common.player.y <= 600: # 상단 문
                if not Stage1_0.stage1_0_create:
                    game_framework.push_mode(stage1_0_mode, (525, 0))
                else:
                    game_framework.pop_mode(stage1_0_mode, (525, 0))
            elif 500 <= common.player.x <=  550 and 0 <= common.player.y <= 20: # 하단 문
                if not Stage1_6.stage1_6_create:
                    game_framework.push_mode(stage1_6_mode, (525, 600))
                else:
                    game_framework.pop_mode(stage1_6_mode, (525, 600))
        else:
            common.player.handle_event(event)

def init(player_start_pos=None):
    global world, slime_mobs, coins
    global stage1_3
    global player
    global ui

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage1_3 = Stage1_3()

    if not Stage1_3.stage1_3_create:
        Stage1_3.stage1_3_create = True
        Stage1_3.current_mode = True

        slime_mobs = [Slime_Mob() for _ in range(random.randint(0, 2))]
        for slime_mob in slime_mobs:
            slime_mob.move_validator = stage1_3.is_mob_walkable

        coins = []
    else:
        slime_mobs = []
        coins = []

    game_world.add_object(stage1_3, 0)

    common.player = Player()
    common.player.move_validator = stage1_3.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(common.player, 2)

    game_world.add_collision_pair('player:coin', common.player, None)

    # 첫 방문 시에만 몹 추가
    if slime_mobs:
        game_world.add_objects(slime_mobs, 2)
        game_world.add_collision_pair('player:slime_mob', common.player, None)
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
        game_world.add_collision_pair('player:coin', common.player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

    ui = Ui()
    game_world.add_object(ui, 4)

def update():
    if Ui.paused:
        return

    game_world.update()
    game_world.handle_collsions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    global slime_mobs, stage1_3, coins
    global ui

    Stage1_3.current_mode = False

    # 기존 saved_mobs 초기화 후 현재 살아있는 몹만 저장
    stage1_3.saved_mobs = []
    for slime_mob in slime_mobs:
        if slime_mob.is_alive:
            stage1_3.saved_mobs.append({
                'type': slime_mob.mob_type,
                'x': slime_mob.x,
                'y': slime_mob.y,
                'hp': slime_mob.hp,
                'frame': slime_mob.frame
            })

    # 코인 저장
    stage1_3.saved_coins = []
    for coin in coins:
        stage1_3.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved {len(stage1_3.saved_mobs)} slime mobs, {len(stage1_3.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()
    ui = None


def resume(player_start_pos=None):
    global slime_mobs, stage1_3, player, coins
    global ui

    Stage1_3.current_mode = True

    common.player.move_validator = stage1_3.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(stage1_3, 0)
    game_world.add_object(common.player, 2)

    # stage1_3 인스턴스에 저장된 몹 복원
    if stage1_3.saved_mobs:
        slime_mobs = []
        for mob_data in stage1_3.saved_mobs:
            slime_mob = Slime_Mob()
            slime_mob.mob_type = mob_data['type']
            slime_mob.x = mob_data['x']
            slime_mob.y = mob_data['y']
            slime_mob.hp = mob_data['hp']
            slime_mob.frame = mob_data['frame']
            slime_mob.move_validator = stage1_3.is_mob_walkable

            slime_mob.move_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.idle_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Jump.png")
            slime_mob.dead_image = load_image("./image/mobs/slime/" + slime_mob.mob_type + "_Slime_Dead.png")

            slime_mobs.append(slime_mob)

        game_world.add_objects(slime_mobs, 2)
        game_world.add_collision_pair('player:slime_mob', common.player, None)
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
    if stage1_3.saved_coins:
        coins = []
        for coin_data in stage1_3.saved_coins:
            coin = Coin()
            coin.x = coin_data['x']
            coin.y = coin_data['y']
            coin.frame = coin_data['frame']
            coins.append(coin)

        game_world.add_objects(coins, 2)

        game_world.add_collision_pair('player:coin', common.player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

        print(f"Resume: Restored {len(slime_mobs)} slime mobs, {len(coins)} coins")
    else:
        print(f"Resume: Restored {len(slime_mobs)} slime mobs, 0 coins")

    ui = Ui()
    game_world.add_object(ui, 4)