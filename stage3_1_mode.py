from pico2d import *

import random
import game_world
import game_framework
import stage3_0_mode, stage3_2_mode
import common
from stage3_1 import Stage3_1
from stage3_0 import Stage3_0
from stage3_2 import Stage3_2
from player import Player
from goblin_mob import Goblin_Mob
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
                if not Stage3_2.stage3_2_create:
                    game_framework.push_mode(stage3_2_mode,(50, 320))
                else:
                    game_framework.pop_mode(stage3_2_mode,(50, 320))
            elif 50 <= common.player.x <= 70 and 270 <= common.player.y <= 370:  # 좌측 문
                if not Stage3_0.stage3_0_create:
                    game_framework.push_mode(stage3_0_mode, (1010, 320))
                else:
                    game_framework.pop_mode(stage3_0_mode, (1010, 320))
        else:
            common.player.handle_event(event)

def init(player_start_pos=None):
    global world, goblin_mobs, coins
    global stage3_1
    global player
    global ui

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage3_1 = Stage3_1()

    if not Stage3_1.stage3_1_create:
        Stage3_1.stage3_1_create = True
        Stage3_1.current_mode = True

        goblin_mobs = [Goblin_Mob() for _ in range(random.randint(2, 5))]
        for goblin_mob in goblin_mobs:
            goblin_mob.move_validator = stage3_1.is_mob_walkable

        coins = []
    else:
        goblin_mobs = []
        coins = []

    game_world.add_object(stage3_1, 0)

    common.player = Player()
    common.player.move_validator = stage3_1.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(common.player, 2)

    game_world.add_collision_pair('player:coin', common.player, None)

    # 첫 방문 시에만 몹 추가
    if goblin_mobs:
        game_world.add_objects(goblin_mobs, 2)
        game_world.add_collision_pair('player:goblin_mob', common.player, None)
        for goblin_mob in goblin_mobs:
            game_world.add_collision_pair('player:goblin_mob', None, goblin_mob)
            game_world.add_collision_pair('goblin_mob:goblin_mob', goblin_mob, None)

            # 다른 몹들과의 충돌 페어 추가
            for goblin_mob in goblin_mobs:
                for other_mob in goblin_mobs:
                    if goblin_mob != other_mob:
                        game_world.add_collision_pair('goblin_mob:goblin_mob', None, other_mob)

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
    global goblin_mobs, stage3_1, coins
    global ui

    Stage3_1.current_mode = False

    # 기존 goblin_mobs 초기화 후 현재 살아있는 몹만 저장
    stage3_1.saved_mobs = []
    for goblin_mob in goblin_mobs:
        if goblin_mob.is_alive:
            mob_data = {
                'x': goblin_mob.x,
                'y': goblin_mob.y,
                'hp': goblin_mob.hp,
                'face_dir': goblin_mob.face_dir,
                'type': goblin_mob.mob_type
            }
            stage3_1.saved_mobs.append(mob_data)
            # print(f"Pause: Saved mob at ({mob_data['x']}, {mob_data['y']}) with type '{mob_data['type']}', HP: {mob_data['hp']}")

    # 코인 저장
    stage3_1.saved_coins = []
    for coin in coins:
        stage3_1.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    # print(f"Pause: Saved {len(stage3_1.saved_mobs)} zombie mobs, {len(stage3_1.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()
    ui = None


def resume(player_start_pos=None):
    global goblin_mobs, stage3_1, player, coins
    global ui

    Stage3_1.current_mode = True

    common.player.move_validator = stage3_1.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(stage3_1, 0)
    game_world.add_object(common.player, 2)

    # 저장된 몹 복원
    if stage3_1.saved_mobs:
        goblin_mobs = []
        for mob_data in stage3_1.saved_mobs:
            # print(f"Resume: Restoring mob with type '{mob_data['type']}' at ({mob_data['x']}, {mob_data['y']})")

            goblin_mob = Goblin_Mob()

            # 저장된 타입으로 설정
            goblin_mob.mob_type = mob_data['type']
            # print(f"Resume: Set mob_type to '{goblin_mob.mob_type}'")

            # 타입에 맞는 이미지 재로드
            goblin_mob.move_image = load_image("./image/mobs/goblin/" + goblin_mob.mob_type + "/walk.png")
            goblin_mob.idle_image = load_image("./image/mobs/goblin/" + goblin_mob.mob_type + "/idle.png")
            goblin_mob.dead_image = load_image("./image/mobs/goblin/" + goblin_mob.mob_type + "/dead.png")
            goblin_mob.attack_image = load_image("./image/mobs/goblin/" + goblin_mob.mob_type + "/attack.png")

            # 위치 및 상태 복원
            goblin_mob.x = mob_data['x']
            goblin_mob.y = mob_data['y']
            goblin_mob.hp = mob_data['hp']
            goblin_mob.face_dir = mob_data.get('face_dir', 0)
            goblin_mob.move_validator = stage3_1.is_mob_walkable

            goblin_mobs.append(goblin_mob)

        game_world.add_objects(goblin_mobs, 2)
        game_world.add_collision_pair('player:goblin_mob', common.player, None)
        for goblin_mob in goblin_mobs:
            game_world.add_collision_pair('player:goblin_mob', None, goblin_mob)
            game_world.add_collision_pair('goblin_mob:goblin_mob', goblin_mob, None)

        for goblin_mob in goblin_mobs:
            for other_mob in goblin_mobs:
                if goblin_mob != other_mob:
                    game_world.add_collision_pair('goblin_mob:goblin_mob', None, other_mob)

        # print(f"Resume: Total restored {len(goblin_mobs)} goblin mobs")
    else:
        pass
        # print("Resume: No saved mobs to restore")

    # 코인 복원
    if stage3_1.saved_coins:
        coins = []
        for coin_data in stage3_1.saved_coins:
            from coin import Coin
            coin = Coin()
            coin.x = coin_data['x']
            coin.y = coin_data['y']
            coin.frame = coin_data['frame']
            coins.append(coin)

        game_world.add_objects(coins, 2)
        game_world.add_collision_pair('player:coin', common.player, None)
        for coin in coins:
            game_world.add_collision_pair('player:coin', None, coin)

        # print(f"Resume: Restored {len(coins)} coins")

    ui = Ui()
    game_world.add_object(ui, 4)