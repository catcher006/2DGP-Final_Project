from pico2d import *

import random
import game_world
import game_framework
import stage2_6_mode, stage2_10_mode
from stage2_9 import Stage2_9
from stage2_6 import Stage2_6
from stage2_10 import Stage2_10
from player import Player
from zombie_mob import Zombie_Mob
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
            if 500 <= player.x <= 550 and 580 <= player.y <= 600:  # 상단 문
                if not Stage2_6.stage2_6_create:
                    game_framework.push_mode(stage2_6_mode, (525, 0))
                else:
                    game_framework.pop_mode(stage2_6_mode, (525, 0))
            elif 990 <= player.x <= 1010 and 270 <= player.y <= 370:  # 우측 문
                if not Stage2_10.stage2_10_create:
                    game_framework.push_mode(stage2_10_mode, (50, 320))
                else:
                    game_framework.pop_mode(stage2_10_mode, (50, 320))
        else:
            player.handle_event(event)

def init(player_start_pos=None):
    global world, zombie_mobs, coins
    global stage2_9
    global player

    # 기존 충돌 페어 초기화
    game_world.collision_pairs.clear()

    stage2_9 = Stage2_9()

    if not Stage2_9.stage2_9_create:
        Stage2_9.stage2_9_create = True
        Stage2_9.current_mode = True

        zombie_mobs = [Zombie_Mob() for _ in range(random.randint(2, 5))]
        for zombie_mob in zombie_mobs:
            zombie_mob.move_validator = stage2_9.is_mob_walkable

        coins = []
    else:
        zombie_mobs = []
        coins = []

    game_world.add_object(stage2_9, 0)

    player = Player()
    player.move_validator = stage2_9.is_walkable
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
            game_world.add_collision_pair('zombie_mob:zombie_mob', zombie_mob, None)

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
    global zombie_mobs, stage2_9, coins

    Stage2_9.current_mode = False

    # 기존 zombie_mobs 초기화 후 현재 살아있는 몹만 저장
    stage2_9.saved_mobs = []
    for zombie_mob in zombie_mobs:
        if zombie_mob.is_alive:
            mob_data = {
                'x': zombie_mob.x,
                'y': zombie_mob.y,
                'hp': zombie_mob.hp,
                'face_dir': zombie_mob.face_dir,
                'type': zombie_mob.mob_type
            }
            stage2_9.saved_mobs.append(mob_data)
            print(f"Pause: Saved mob at ({mob_data['x']}, {mob_data['y']}) with type '{mob_data['type']}', HP: {mob_data['hp']}")

    # 코인 저장
    stage2_9.saved_coins = []
    for coin in coins:
        stage2_9.saved_coins.append({
            'x': coin.x,
            'y': coin.y,
            'frame': coin.frame
        })

    print(f"Pause: Saved {len(stage2_9.saved_mobs)} zombie mobs, {len(stage2_9.saved_coins)} coins")

    game_world.clear()
    game_world.collision_pairs.clear()


def resume(player_start_pos=None):
    global zombie_mobs, stage2_9, player, coins

    Stage2_9.current_mode = True

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(stage2_9, 0)
    game_world.add_object(player, 2)

    # 저장된 몹 복원
    if stage2_9.saved_mobs:
        zombie_mobs = []
        for mob_data in stage2_9.saved_mobs:
            print(f"Resume: Restoring mob with type '{mob_data['type']}' at ({mob_data['x']}, {mob_data['y']})")

            zombie_mob = Zombie_Mob()

            # 저장된 타입으로 설정
            zombie_mob.mob_type = mob_data['type']
            print(f"Resume: Set mob_type to '{zombie_mob.mob_type}'")

            # 타입에 맞는 이미지 재로드
            zombie_mob.move_image = load_image("./image/mobs/zombie/" + zombie_mob.mob_type + "/walk.png")
            zombie_mob.idle_image = load_image("./image/mobs/zombie/" + zombie_mob.mob_type + "/idle.png")
            zombie_mob.dead_image = load_image("./image/mobs/zombie/" + zombie_mob.mob_type + "/dead.png")
            if zombie_mob.mob_type == 'mace':
                zombie_mob.attack_image = load_image("./image/mobs/zombie/" + zombie_mob.mob_type + "/attack.png")

            # 위치 및 상태 복원
            zombie_mob.x = mob_data['x']
            zombie_mob.y = mob_data['y']
            zombie_mob.hp = mob_data['hp']
            zombie_mob.face_dir = mob_data.get('face_dir', 0)
            zombie_mob.move_validator = stage2_9.is_mob_walkable

            # 타입에 맞는 state_machine 재구성
            from state_machine import StateMachine
            from zombie_mob import Idle, Move, Dead, Attack, time_out, event_stop, event_die

            zombie_mob.IDLE = Idle(zombie_mob)
            zombie_mob.MOVE = Move(zombie_mob)
            zombie_mob.DEAD = Dead(zombie_mob)

            if zombie_mob.mob_type == "mace":
                zombie_mob.ATTACK = Attack(zombie_mob)
                zombie_mob.state_machine = StateMachine(
                    zombie_mob.IDLE,
                    {
                        zombie_mob.IDLE: {time_out: zombie_mob.MOVE, event_die: zombie_mob.DEAD},
                        zombie_mob.MOVE: {event_die: zombie_mob.DEAD, event_stop: zombie_mob.ATTACK},
                        zombie_mob.ATTACK: {time_out: zombie_mob.MOVE, event_die: zombie_mob.DEAD},
                        zombie_mob.DEAD: {}
                    }
                )
                print(f"Resume: Created state_machine with ATTACK state for mace type")
            else:
                zombie_mob.state_machine = StateMachine(
                    zombie_mob.IDLE,
                    {
                        zombie_mob.MOVE: {event_die: zombie_mob.DEAD, event_stop: zombie_mob.IDLE},
                        zombie_mob.IDLE: {time_out: zombie_mob.MOVE, event_die: zombie_mob.DEAD},
                        zombie_mob.DEAD: {}
                    }
                )
                print(f"Resume: Created state_machine without ATTACK state for none type")

            # IDLE 상태로 명시적 전환
            zombie_mob.state_machine.cur_state = zombie_mob.IDLE
            zombie_mob.IDLE.enter(None)

            print(f"Resume: Mob restored - Type: '{zombie_mob.mob_type}', Position: ({zombie_mob.x}, {zombie_mob.y}), HP: {zombie_mob.hp}")
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

        print(f"Resume: Total restored {len(zombie_mobs)} zombie mobs")
    else:
        print("Resume: No saved mobs to restore")

    # 코인 복원
    if stage2_9.saved_coins:
        coins = []
        for coin_data in stage2_9.saved_coins:
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