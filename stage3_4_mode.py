from pico2d import *

import random
import game_world
import game_framework
import stage3_3_mode, stage3_7_mode
from stage3_4 import Stage3_4
from stage3_3 import Stage3_3
from stage3_7 import Stage3_7
from player import Player
from goblin_mob import Goblin_Mob
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
            if 50 <= player.x <= 70 and 270 <= player.y <= 370:  # 좌측 문
                if not Stage3_3.stage3_3_create:
                    game_framework.push_mode(stage3_3_mode, (1010, 320))
                else:
                    game_framework.pop_mode(stage3_3_mode, (1010, 320))
            elif 500 <= player.x <=  550 and 0 <= player.y <= 20: # 하단 문
                if not Stage3_7.stage3_7_create:
                    game_framework.push_mode(stage3_7_mode, (525, 600))
                else:
                    game_framework.pop_mode(stage3_7_mode, (525, 600))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world, goblin_mobs, coins
    global stage3_4
    global player

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage3_4 = Stage3_4()

    if not Stage3_4.stage3_4_create:
        Stage3_4.stage3_4_create = True
        Stage3_4.current_mode = True

        goblin_mobs = [Goblin_Mob() for _ in range(random.randint(2, 5))]
        for goblin_mob in goblin_mobs:
            goblin_mob.move_validator = stage3_4.is_mob_walkable

        coins = []
    else:
        goblin_mobs = []
        coins = []

    game_world.add_object(stage3_4, 0)

    player = Player()
    player.move_validator = stage3_4.is_walkable
    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(player, 2)

    game_world.add_collision_pair('player:coin', player, None)

    # 첫 방문 시에만 몹 추가
    if goblin_mobs:
        game_world.add_objects(goblin_mobs, 2)
        game_world.add_collision_pair('player:goblin_mob', player, None)
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
    global goblin_mobs, stage3_4, coins

    Stage3_4.current_mode = False

    # 기존 goblin_mobs 초기화 후 현재 살아있는 몹만 저장
    stage3_4.saved_mobs = []
    for goblin_mob in goblin_mobs:
        if goblin_mob.is_alive:
            mob_data = {
                'x': goblin_mob.x,
                'y': goblin_mob.y,
                'hp': goblin_mob.hp,
                'face_dir': goblin_mob.face_dir,
                'type': goblin_mob.mob_type
            }
            stage3_4.saved_mobs.append(mob_data)
            print(f"Pause: Saved mob at ({mob_data['x']}, {mob_data['y']}) with type '{mob_data['type']}', HP: {mob_data['hp']}")

    # 코인 미저장 버그 부분을 찾지 못해서 임시 방편으로 월드에서 코인 객체를 다시 수집
    from coin import Coin

    present_coins = []
    for layer in game_world.world:
        for obj in layer:
            if isinstance(obj, Coin):
                present_coins.append(obj)

    # 모듈 변수 coins를 실제 월드 상태와 동기화
    coins = present_coins

    # 코인 저장
    stage3_4.saved_coins = []
    for coin in coins:
        stage3_4.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved {len(stage3_4.saved_mobs)} zombie mobs, {len(stage3_4.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()


def resume(player_start_pos=None):
    global goblin_mobs, stage3_4, player, coins

    Stage3_4.current_mode = True

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(stage3_4, 0)
    game_world.add_object(player, 2)

    # 저장된 몹 복원
    if stage3_4.saved_mobs:
        goblin_mobs = []
        for mob_data in stage3_4.saved_mobs:
            print(f"Resume: Restoring mob with type '{mob_data['type']}' at ({mob_data['x']}, {mob_data['y']})")

            goblin_mob = Goblin_Mob()

            # 저장된 타입으로 설정
            goblin_mob.mob_type = mob_data['type']
            print(f"Resume: Set mob_type to '{goblin_mob.mob_type}'")

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
            goblin_mob.move_validator = stage3_4.is_mob_walkable

            goblin_mobs.append(goblin_mob)

        game_world.add_objects(goblin_mobs, 2)
        game_world.add_collision_pair('player:goblin_mob', player, None)
        for goblin_mob in goblin_mobs:
            game_world.add_collision_pair('player:goblin_mob', None, goblin_mob)
            game_world.add_collision_pair('goblin_mob:goblin_mob', goblin_mob, None)

        for goblin_mob in goblin_mobs:
            for other_mob in goblin_mobs:
                if goblin_mob != other_mob:
                    game_world.add_collision_pair('goblin_mob:goblin_mob', None, other_mob)

        print(f"Resume: Total restored {len(goblin_mobs)} goblin mobs")
    else:
        print("Resume: No saved mobs to restore")

    # 코인 복원
    if stage3_4.saved_coins:
        coins = []
        for coin_data in stage3_4.saved_coins:
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