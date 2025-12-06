from pico2d import *

import game_world
import game_framework
import stage1_5_mode
import stage1_7_mode
import common
from stage1_4 import Stage1_4
from stage1_5 import Stage1_5
from stage1_7 import Stage1_7
from player import Player
from slime_boss import Slime_Boss
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
            if 990 <= common.player.x <=  1010 and 270 <= common.player.y <= 370: # 우측 문
                if not Stage1_5.stage1_5_create:
                    game_framework.push_mode(stage1_5_mode,(50, 320))
                else:
                    game_framework.pop_mode(stage1_5_mode, (50, 320))
            elif 500 <= common.player.x <=  550 and 0 <= common.player.y <= 20: # 하단 문
                if not Stage1_7.stage1_7_create:
                    game_framework.push_mode(stage1_7_mode, (525, 600))
                else:
                    game_framework.pop_mode(stage1_7_mode, (525, 600))
        else:
            common.player.handle_event(event)

def init(player_start_pos=None):
    global world, slime_boss, coins
    global stage1_4
    global player
    global ui

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage1_4 = Stage1_4()

    if not Stage1_4.stage1_4_create:
        Stage1_4.stage1_4_create = True
        Stage1_4.current_mode = True

        slime_boss = Slime_Boss()
        slime_boss.move_validator = stage1_4.is_mob_walkable

        coins = []
    else:
        slime_boss = None
        coins = []

    game_world.add_object(stage1_4, 0)

    common.player = Player()
    common.player.move_validator = stage1_4.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(common.player, 2)

    game_world.add_collision_pair('player:coin', common.player, None)

    # 첫 방문 시에만 몹 추가
    if slime_boss:
        game_world.add_object(slime_boss, 2)
        game_world.add_collision_pair('player:slime_boss', common.player, None)
        game_world.add_collision_pair('player:slime_boss', None, slime_boss)

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
    global slime_boss, stage1_4, coins
    global ui

    Stage1_4.current_mode = False

    # 기존 saved_mobs 초기화 후 현재 살아있는 몹만 저장
    stage1_4.saved_mobs = []
    if slime_boss is not None and slime_boss.is_alive:
        stage1_4.saved_mobs.append({
            'x': slime_boss.x,
            'y': slime_boss.y,
            'hp': slime_boss.hp,
            'frame': slime_boss.frame
        })
        print(f"Pause: Saved boss (hp: {slime_boss.hp})")
    else:
        print("Pause: No boss to save")

    # 코인 저장
    stage1_4.saved_coins = []
    for coin in coins:
        stage1_4.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved boss (alive: {slime_boss.is_alive if slime_boss else False}), {len(stage1_4.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()
    ui = None


def resume(player_start_pos=None):
    global slime_boss, stage1_4, player, coins
    global ui

    Stage1_4.current_mode = True

    common.player.move_validator = stage1_4.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(stage1_4, 0)
    game_world.add_object(common.player, 2)

    # 저장된 보스 복원
    if stage1_4.saved_mobs:
        mob_data = stage1_4.saved_mobs[0]  # 보스는 1마리만
        slime_boss = Slime_Boss()
        slime_boss.x = mob_data['x']
        slime_boss.y = mob_data['y']
        slime_boss.hp = mob_data['hp']
        slime_boss.frame = mob_data['frame']
        slime_boss.move_validator = stage1_4.is_mob_walkable

        game_world.add_object(slime_boss, 2)
        game_world.add_collision_pair('player:slime_boss', common.player, None)
        game_world.add_collision_pair('player:slime_boss', None, slime_boss)

        print(f"Resume: Restored boss")
    else:
        slime_boss = None
        print("Resume: No saved boss to restore")

    # 코인 복원
    if stage1_4.saved_coins:
        coins = []
        for coin_data in stage1_4.saved_coins:
            coin = Coin()
            coin.x = coin_data['x']
            coin.y = coin_data['y']
            coin.frame = coin_data['frame']
            coins.append(coin)

        game_world.add_objects(coins, 2)

        game_world.add_collision_pair('player:coin', common.player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

        print(f"Resume: Restored {len(coins)} coins")
    else:
        print(f"Resume: 0 coins")

    ui = Ui()
    game_world.add_object(ui, 4)