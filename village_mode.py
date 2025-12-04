from pico2d import *

import dungeonmain_mode
import game_world
import game_framework
import title_mode
import random
import common
from village import Village
from village_front_object import Village_Front_Object
from player import Player
from ui import Ui

enhance_active = False # 강화 모드 활성화 플래그
font = None

# 강화 시스템 설정
TIER_LIST = ['normal', 'silver', 'gold']
COSTS = {'none': 500, 'normal': 800, 'silver': 1000 }
ODDS = {'none': 0.6, 'normal': 0.3, 'silver': 0.1 }

BUTTONS = {
    'sword': (150, 150, 150, 50),
    'arrow': (450, 150, 150, 50),
    'shield': (750, 150, 150, 50)
}

# 버튼 애니메이션 상태
button_animations = {
    'sword': {'frame': 0, 'animating': False, 'time': 0, 'sequence_index': 0},
    'arrow': {'frame': 0, 'animating': False, 'time': 0, 'sequence_index': 0},
    'shield': {'frame': 0, 'animating': False, 'time': 0, 'sequence_index': 0}
}

coin_warning = {
    'active': False,
    'frame': 0,
    'sequence_index': 0,
    'time': 0
}

BUTTON_FRAME_SEQUENCE = [0, 1, 2, 1, 0]
BUTTON_FRAME_TIME = 0.1
COIN_WARNING_SEQUENCE = [0, 1, 2, 3, 4, 3, 2, 1, 0]
COIN_WARNING_FRAME_TIME = 0.07

def point_in_rect(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def get_current_tier(item_name):
    """현재 아이템 등급 반환 (속성 안전 조회)"""
    p = getattr(common, 'player', None)
    if not p:
        return 'none'

    if item_name == 'sword':
        sword_id = common.player.player_sword_id
        if 'gold' in sword_id:
            return 'gold'
        elif 'silver' in sword_id:
            return 'silver'
        elif 'normal' in sword_id:
            return 'normal'
        return 'none'
    elif item_name == 'arrow':
        bow_id = common.player.player_bow_id
        if 'gold' in bow_id:
            return 'gold'
        elif 'silver' in bow_id:
            return 'silver'
        elif 'normal' in bow_id:
            return 'normal'
        return 'none'
    elif item_name == 'shield':
        plate_id = common.player.player_plate_id
        if 'gold' in plate_id:
            return 'gold'
        elif 'silver' in plate_id:
            return 'silver'
        elif 'normal' in plate_id:
            return 'normal'
        return 'none'

    return 'none'


def start_button_animation(button_name):
    """버튼 애니메이션 시작 (frame/sequence 초기화)"""
    anim = button_animations.get(button_name)
    if not anim:
        return
    anim['animating'] = True
    anim['time'] = 0
    anim['sequence_index'] = 0
    anim['frame'] = BUTTON_FRAME_SEQUENCE[0] if BUTTON_FRAME_SEQUENCE else 0


def update_button_animations():
    """버튼 애니메이션 업데이트 (키 존재 안전 처리)"""
    for name, anim in button_animations.items():
        if anim.get('animating'):
            anim['time'] += game_framework.frame_time

            if anim['time'] >= BUTTON_FRAME_TIME:
                anim['time'] = 0
                # 안전하게 sequence_index 증가
                anim['sequence_index'] = anim.get('sequence_index', 0) + 1

                if anim['sequence_index'] >= len(BUTTON_FRAME_SEQUENCE):
                    anim['animating'] = False
                    anim['sequence_index'] = 0
                    anim['frame'] = 0
                else:
                    anim['frame'] = BUTTON_FRAME_SEQUENCE[anim['sequence_index']]

def start_coin_warning():
    """코인 부족 경고 애니메이션 시작"""
    coin_warning['active'] = True
    coin_warning['time'] = 0
    coin_warning['sequence_index'] = 0
    coin_warning['frame'] = 0


def update_coin_warning():
    """코인 부족 경고 애니메이션 업데이트"""
    if coin_warning['active']:
        coin_warning['time'] += game_framework.frame_time

        if coin_warning['time'] >= COIN_WARNING_FRAME_TIME:
            coin_warning['time'] = 0
            coin_warning['sequence_index'] += 1

            if coin_warning['sequence_index'] >= len(COIN_WARNING_SEQUENCE):
                coin_warning['active'] = False
                coin_warning['sequence_index'] = 0
                coin_warning['frame'] = 0
            else:
                coin_warning['frame'] = COIN_WARNING_SEQUENCE[coin_warning['sequence_index']]


def enhance_item(item_type):
    """아이템 강화 시도"""
    current_tier = get_current_tier(item_type)

    if current_tier == 'gold':
        print(f"{item_type} is already max tier!")
        return False

    success_rates = {
        'none': 0.6,
        'normal': 0.3,
        'silver': 0.1
    }
    success_rate = success_rates.get(current_tier, 0)

    if random.random() < success_rate:
        if current_tier == 'none':
            next_tier = 'normal'
        else:
            try:
                next_tier = TIER_LIST[TIER_LIST.index(current_tier) + 1]
            except (ValueError, IndexError):
                print("Tier calculation error")
                return False

        if not getattr(common, 'player', None):
            print("No player to enhance")
            return False

        # 등급 적용
        if item_type == 'sword':
            new_sword_id = f'{next_tier}_sword'
            Player.player_sword_id = new_sword_id
            Player.current_weapon_id = new_sword_id
            print(f"[DEBUG] Sword enhanced:")
            print(f"  - player_sword_id: {Player.player_sword_id}")
            print(f"  - current_weapon_id: {Player.current_weapon_id}")
        elif item_type == 'arrow':
            new_bow_id = f'{next_tier}_bow'
            Player.player_bow_id = new_bow_id
            Player.current_weapon_id = new_bow_id
            print(f"[DEBUG] Bow enhanced:")
            print(f"  - player_bow_id: {Player.player_bow_id}")
            print(f"  - current_weapon_id: {Player.current_weapon_id}")
        elif item_type == 'shield':
            Player.player_plate_id = f'{next_tier}_plate'

        reload_player_images()

        print(f"Enhancement SUCCESS! {item_type} -> {next_tier}")
        return True
    else:
        print(f"Enhancement FAILED for {item_type}")
        return False


def reload_player_images():
    """플레이어 이미지를 새로 로드"""
    if not getattr(common, 'player', None):
        print("reload_player_images: common.player is None")
        return

    # 이미지 재로드
    common.player.load_walk_images()
    common.player.load_idle_images()
    common.player.load_dead_images()
    common.player.load_combat_idle_images()

    weapon_type = common.player.check_weapon()
    if weapon_type == 'sword':
        common.player.load_sword_images()
    elif weapon_type == 'bow':
        common.player.load_bow_images()

    print(f"Player images reloaded: plate={Player.player_plate_id}, weapon={Player.current_weapon_id}")


def handle_enhance_click(mx, my):
    """버튼 클릭 처리"""
    print(f"Checking click at ({mx}, {my})")
    for name, rect in BUTTONS.items():
        print(f"  Button '{name}': {rect}")
        if point_in_rect(mx, my, rect):
            print(f"  -> Clicked {name} button!")

            # 현재 등급 확인
            tier = get_current_tier(name)
            cost = COSTS.get(tier, 'MAX')

            # 최대 등급이 아니고 돈이 충분한지 확인
            if cost != 'MAX':
                if Ui.coin >= cost:
                    # 버튼 애니메이션 시작
                    start_button_animation(name)

                    # 강화 시도
                    if enhance_item(name):
                        # 성공: 돈 차감
                        Ui.coin -= cost
                        print(f"Enhancement successful! Remaining coins: {Ui.coin}")
                    else:
                        # 실패: 돈만 차감
                        Ui.coin -= cost
                        print(f"Enhancement failed! Remaining coins: {Ui.coin}")
                else:
                    # 돈이 부족하면 경고 애니메이션 시작
                    print("Not enough coins!")
                    start_coin_warning()
            else:
                print(f"{name} is already at max tier!")
            return
    print("  -> No button clicked")


def draw_button(name, rect):
    x, y, w, h = rect
    cx = x + w // 2
    cy = y + h // 2

    frame = button_animations.get(name, {}).get('frame', 0)
    print(f"Drawing {name} button with frame {frame}")

    # village가 없으면 그리기 시도하지 않음
    if 'village' in globals() and getattr(village, 'button_start', None):
        village.button_start.clip_draw(320 * frame, 0, 320, 115, cx, cy, w, h)

    if font:
        tier = get_current_tier(name)
        cost = COSTS.get(tier, 'MAX')

        item_name = ''
        p = getattr(common, 'player', None)
        if p:
            if name == 'sword':
                item_name = getattr(p, 'player_sword_id', 'NONE').replace('_', ' ').upper()
            elif name == 'arrow':
                item_name = getattr(p, 'player_bow_id', 'NONE').replace('_', ' ').upper()
            elif name == 'shield':
                item_name = getattr(p, 'player_plate_id', 'NONE').replace('_', ' ').upper()
        else:
            item_name = 'NONE'

        font.draw(x, y + h + 80, f'{name.upper()} [{tier.upper()}]', (255, 255, 255))

        if item_name != 'NONE':
            font.draw(cx - 50, cy, item_name, (255, 200, 0))
        else:
            font.draw(cx - 30, cy, 'EMPTY', (150, 150, 150))

        if cost != 'MAX':
            success_rates = {'none': '60%', 'normal': '30%', 'silver': '10%'}
            rate = success_rates.get(tier, '0%')
            font.draw(x + 10, y + h + 15, f'Cost: {cost} | Rate: {rate}', (255, 255, 0))
        else:
            font.draw(cx - 20, y + h + 15, 'MAX', (0, 255, 0))

def handle_events():
    global running, enhance_active

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            if enhance_active:
                enhance_active = False # 강화 모드 비활성화
            else:
                game_framework.change_mode(title_mode)
        elif enhance_active:
            # 강화 UI가 활성화되어 있으면 마우스 클릭만 처리
            if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                # 마우스 y 좌표를 화면 좌표계로 변환
                mx = event.x
                my = get_canvas_height() - event.y
                print(f"Mouse clicked at: ({mx}, {my})")  # 디버그용
                handle_enhance_click(mx, my)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if 480 <= common.player.x <= 590 and 370 <= common.player.y <= 380: # 던전 입구 좌표 범위
                game_framework.push_mode(dungeonmain_mode,(535, 60))
            elif 210 <= common.player.x <= 260 and 190 <= common.player.y <= 210:  # 짐 좌표 범위 - 아이템 강화
                enhance_active = True # 강화 모드 활성화
        else:
            common.player.handle_event(event)

def draw_enhance_ui():
    # 반투명 배경 (선택사항)
    village.black_screen.clip_draw(5 * 768, 0, 768, 144, 512, 288, 1024, 576)

    if font:
        font.draw(400, 500, '=== Enhance Menu ===', (255, 255, 255))

        for name, rect in BUTTONS.items():
            draw_button(name, rect)

        coins_text = f'Your coins: {Ui.coin}'
        font.draw(120, 120, coins_text, (255, 255, 255))
        font.draw(120, 80, 'ESC to close  -  Click to enhance', (180, 180, 180))

    # 코인 부족 경고 표시
    if coin_warning['active']:
        frame = coin_warning['frame']
        village.info_coin.clip_draw(0, frame * 78, 490, 78, 512, 288)

def init(player_start_pos=None):
    global world
    global village
    global player
    global back_object
    global front_object
    global enhance_active
    global font

    enhance_active = False
    font = load_font('ENCR10B.TTF', 20)

    village = Village()
    game_world.add_object((village), 0)

    # back_object = Village_Back_Object()
    # game_world.add_object((back_object), 1)

    common.player = Player()
    # 마을 모드에서 이동 검사 콜백을 마을 객체에 위임
    common.player.move_validator = village.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos
    else:
        common.player.x, common.player.y = 510, 160  # 기본 좌표
    game_world.add_object((common.player), 2)

    front_object = Village_Front_Object()
    game_world.add_object((front_object), 3)

    ui = Ui()
    game_world.add_object(ui, 4)

def update():
    if enhance_active:
        update_button_animations()
        update_coin_warning()
    else:
        game_world.update()

def draw():
    clear_canvas()
    game_world.render()

    # 강화 UI 오버레이
    if enhance_active:
        draw_enhance_ui()

    update_canvas()

def finish():
    game_world.clear()

def pause():
    # 현재 모드의 모든 객체를 게임 월드에서 제거
    game_world.clear()
    # 충돌 페어도 정리
    game_world.collision_pairs.clear()

def resume(player_start_pos=None):
    # 필요시 village 객체들을 다시 초기화
    global village, back_object, front_object, player

    common.player.move_validator = village.is_walkable
    if player_start_pos:
        common.player.x, common.player.y = player_start_pos

    game_world.add_object(village, 0)
    game_world.add_object(common.player, 2)
    game_world.add_object(front_object, 3)

    ui = Ui()
    game_world.add_object(ui, 4)
