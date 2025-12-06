from pico2d import *

import game_world
import game_framework
import stage3_4_mode
import common
from stage3_7 import Stage3_7
from stage3_4 import Stage3_4
from player import Player
from goblin_boss import Goblin_Boss
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
            if 500 <= common.player.x <=  550 and 580 <= common.player.y <= 600: # 상단 문 (메인 던전으로 가는 문)
                if not Stage3_4.stage3_4_create:
                    game_framework.push_mode(stage3_4_mode,(525, 0))
                else:
                    game_framework.pop_mode(stage3_4_mode,(525, 0))
        else:
            common.player.handle_event(event)

def init(player_start_pos=None):
    global world, goblin_boss, coins
    global stage3_7
    global player
    global ui

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage3_7 = Stage3_7()

    if not Stage3_7.stage3_7_create:
        Stage3_7.stage3_7_create = True
        Stage3_7.current_mode = True

        goblin_boss = Goblin_Boss()
        goblin_boss.move_validator = stage3_7.is_mob_walkable

        coins = []
    else:
        goblin_boss = []
        coins = []

    game_world.add_object(stage3_7, 0)

    common.player = Player()
    common.player.move_validator = stage3_7.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(common.player, 2)

    game_world.add_collision_pair('player:coin', common.player, None)

    # 첫 방문 시에만 몹 추가
    if goblin_boss:
        game_world.add_object(goblin_boss, 2)
        game_world.add_collision_pair('player:goblin_boss', common.player, None)
        game_world.add_collision_pair('player:goblin_boss', None, goblin_boss)

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
    global goblin_boss, stage3_7, coins
    global ui

    Stage3_7.current_mode = False

    # 기존 goblin_boss 초기화 후 현재 살아있는 몹만 저장
    stage3_7.saved_mobs = []
    if goblin_boss is not None and goblin_boss.is_alive:
            stage3_7.saved_mobs.append({
                'x': goblin_boss.x,
                'y': goblin_boss.y,
                'hp': goblin_boss.hp,
                'face_dir': goblin_boss.face_dir,
            })

    # 코인 복사 버그 부분을 찾지 못해서 임시 방편으로 월드에서 코인 객체를 다시 수집
    from coin import Coin

    present_coins = []
    for layer in game_world.world:
        for obj in layer:
            if isinstance(obj, Coin):
                present_coins.append(obj)

    # 모듈 변수 coins를 실제 월드 상태와 동기화
    coins = present_coins

    # 코인 저장
    stage3_7.saved_coins = []
    for coin in coins:
        stage3_7.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved {len(stage3_7.saved_mobs)} zombie mobs, {len(stage3_7.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()
    ui = None


def resume(player_start_pos=None):
    global goblin_boss, stage3_7, player, coins
    global ui

    Stage3_7.current_mode = True

    common.player.move_validator = stage3_7.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(stage3_7, 0)
    game_world.add_object(common.player, 2)

    # 저장된 몹 복원
    if stage3_7.saved_mobs:
        mob_data = stage3_7.saved_mobs[0]
        goblin_boss = Goblin_Boss()
        goblin_boss.x = mob_data['x']
        goblin_boss.y = mob_data['y']
        goblin_boss.hp = mob_data['hp']
        goblin_boss.face_dir = mob_data.get('face_dir', 0)
        goblin_boss.move_validator = stage3_7.is_mob_walkable

        game_world.add_object(goblin_boss, 2)
        game_world.add_collision_pair('player:goblin_boss', common.player, None)
        game_world.add_collision_pair('player:goblin_boss', None, goblin_boss)
    else:
        goblin_boss = None
        print("Resume: No saved mobs to restore")

    # 코인 복원
    if stage3_7.saved_coins:
        coins = []
        for coin_data in stage3_7.saved_coins:
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

        print(f"Resume: Restored {len(coins)} coins")

    ui = Ui()
    game_world.add_object(ui, 4)