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
weapon_select = False # 무기 선택 모드 활성화 플래그

# 강화 시스템 설정
TIER_LIST = ['normal', 'silver', 'gold']
COSTS = {'none': 500, 'normal': 800, 'silver': 1000 }
ODDS = {'none': 0.6, 'normal': 0.3, 'silver': 0.1 }

BUTTONS = {
    'sword': (150, 150, 150, 50),
    'arrow': (450, 150, 150, 50),
    'shield': (750, 150, 150, 50)
}

MENU_BUTTONS = {
    'enhance': (20, 450, 64, 64),  # 상단: 강화 버튼
    'weapon': (20, 380, 64, 64)    # 하단: 무기 선택 버튼
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

weapon_warning = {
    'active': False,
    'frame': 0,
    'sequence_index': 0,
    'time': 0
}

already_selected_warning = {
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
    """현재 아이템 등급 반환"""
    if item_name == 'sword':
        sword_id = Player.player_sword_id
        if 'gold' in sword_id:
            return 'gold'
        elif 'silver' in sword_id:
            return 'silver'
        elif 'normal' in sword_id:
            return 'normal'
        return 'none'
    elif item_name == 'arrow':
        bow_id = Player.player_bow_id
        if 'gold' in bow_id:
            return 'gold'
        elif 'silver' in bow_id:
            return 'silver'
        elif 'normal' in bow_id:
            return 'normal'
        return 'none'
    elif item_name == 'shield':
        plate_id = Player.player_plate_id
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

def start_weapon_warning():
    """무기 없음 경고 애니메이션 시작"""
    weapon_warning['active'] = True
    weapon_warning['time'] = 0
    weapon_warning['sequence_index'] = 0
    weapon_warning['frame'] = 0


def update_weapon_warning():
    """무기 없음 경고 애니메이션 업데이트"""
    if weapon_warning['active']:
        weapon_warning['time'] += game_framework.frame_time

        if weapon_warning['time'] >= COIN_WARNING_FRAME_TIME:
            weapon_warning['time'] = 0
            weapon_warning['sequence_index'] += 1

            if weapon_warning['sequence_index'] >= len(COIN_WARNING_SEQUENCE):
                weapon_warning['active'] = False
                weapon_warning['sequence_index'] = 0
                weapon_warning['frame'] = 0
            else:
                weapon_warning['frame'] = COIN_WARNING_SEQUENCE[weapon_warning['sequence_index']]


def start_already_selected_warning():
    """이미 선택된 무기 경고 애니메이션 시작"""
    already_selected_warning['active'] = True
    already_selected_warning['time'] = 0
    already_selected_warning['sequence_index'] = 0
    already_selected_warning['frame'] = 0


def update_already_selected_warning():
    """이미 선택된 무기 경고 애니메이션 업데이트"""
    if already_selected_warning['active']:
        already_selected_warning['time'] += game_framework.frame_time

        if already_selected_warning['time'] >= COIN_WARNING_FRAME_TIME:
            already_selected_warning['time'] = 0
            already_selected_warning['sequence_index'] += 1

            if already_selected_warning['sequence_index'] >= len(COIN_WARNING_SEQUENCE):
                already_selected_warning['active'] = False
                already_selected_warning['sequence_index'] = 0
                already_selected_warning['frame'] = 0
            else:
                already_selected_warning['frame'] = COIN_WARNING_SEQUENCE[already_selected_warning['sequence_index']]


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
            next_tier = TIER_LIST[TIER_LIST.index(current_tier) + 1]

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


def handle_weapon_select_click(mx, my):
    # 무기 선택 클릭 처리
    enhance_rect = MENU_BUTTONS.get('enhance')
    weapon_rect = MENU_BUTTONS.get('weapon')

    if enhance_rect and point_in_rect(mx, my, enhance_rect):
        return
    if weapon_rect and point_in_rect(mx, my, weapon_rect):
        return

    for name in ['sword', 'arrow']:
        rect = BUTTONS.get(name)
        if rect:
            x, y, w, h = rect
            cx = x + w // 2
            icon_y = 300
            icon_size = 100

            icon_cx = cx + 150
            icon_left = icon_cx - icon_size // 2
            icon_right = icon_cx + icon_size // 2
            icon_bottom = icon_y - icon_size // 2
            icon_top = icon_y + icon_size // 2

            if icon_left <= mx <= icon_right and icon_bottom <= my <= icon_top:
                tier = get_current_tier(name)

                # tier가 none이면 경고 애니메이션 시작
                if tier == 'none':
                    start_weapon_warning()
                    print(f"{name} is not available!")
                    return

                # 이미 선택된 무기인지 확인
                if name == 'sword':
                    if 'sword' in Player.current_weapon_id:
                        start_already_selected_warning()
                        print(f"Sword is already selected!")
                        return
                    Player.current_weapon_id = Player.player_sword_id
                    print(f"Sword selected: {Player.current_weapon_id}")
                elif name == 'arrow':
                    if 'bow' in Player.current_weapon_id:
                        start_already_selected_warning()
                        print(f"Bow is already selected!")
                        return
                    Player.current_weapon_id = Player.player_bow_id
                    print(f"Bow selected: {Player.current_weapon_id}")

                reload_player_images()
                return


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

    for menu_name, menu_rect in MENU_BUTTONS.items():
        if point_in_rect(mx, my, menu_rect):
            print(f"  -> Clicked menu button: {menu_name}")
            if menu_name == 'enhance':
                enhance_active = True
                weapon_select = False
                print("Enhance menu activated.")
            elif menu_name == 'weapon':
                weapon_select = True
                enhance_active = False
                print("Weapon selection menu activated.")
            return
    print("  -> No button clicked")

def draw_menu_button(name, rect):
    for name, rect in MENU_BUTTONS.items():
        x, y, w, h = rect
        cx = x + w // 2
        cy = y + h // 2

        # enhance 활성화 시 enhance 버튼 강조, weapon_select 활성화 시 weapon 버튼 강조
        if name == 'enhance':
            frame = 0 if enhance_active else 1
            village.button_enhance.clip_draw(frame * 192, 0, 192, 192, cx, cy, w, h)
        elif name == 'weapon':
            frame = 0 if weapon_select else 1
            village.button_weapon.clip_draw(frame * 192, 0, 192, 192, cx, cy, w, h)


def draw_button(name, rect, mode='enhance'):
    """버튼 그리기 (모드에 따라 다른 스타일)"""
    x, y, w, h = rect
    cx = x + w // 2
    cy = y + h // 2

    # 강화 모드
    if mode == 'enhance':
        frame = button_animations.get(name, {}).get('frame', 0)

        # 아이템 아이콘 표시
        tier = get_current_tier(name)
        icon_y = y + h + 150

        if tier == 'none':
            # 아이콘 대신 [None] 텍스트로 표시
            village.font.draw(cx - 25, icon_y, '[None]', (255, 255, 255))
        else:
            tier_frame = 0
            if tier == 'silver':
                tier_frame = 1
            elif tier == 'gold':
                tier_frame = 2

            if name == 'sword' and village.icon_sword:
                village.icon_sword.clip_draw(tier_frame * 64, 0, 64, 64, cx, icon_y, 100, 100)
            elif name == 'arrow' and village.icon_arrow:
                village.icon_arrow.clip_draw(tier_frame * 64, 0, 64, 64, cx, icon_y, 100, 100)
            elif name == 'shield' and village.icon_shield:
                village.icon_shield.clip_draw(tier_frame * 64, 0, 64, 64, cx, icon_y, 100, 100)

        # 버튼 그리기
        village.button_start.clip_draw(320 * frame, 0, 320, 115, cx, cy, w, h)

        # 아이템 이름 표시
        if name == 'sword':
            item_name = Player.player_sword_id.replace('_', ' ').upper()
        elif name == 'arrow':
            item_name = Player.player_bow_id.replace('_', ' ').upper()
        elif name == 'shield':
            item_name = Player.player_plate_id.replace('_', ' ').upper()
        else:
            item_name = 'NONE'

        if item_name != 'NONE':
            text_width = len(item_name) * 10
            village.font.draw(cx - text_width // 2, cy + 45, item_name, (255, 200, 0))

        tier = get_current_tier(name)
        cost = COSTS.get(tier, 'MAX')
        if cost != 'MAX':
            success_rates = {'none': '60%', 'normal': '30%', 'silver': '10%'}
            rate = success_rates.get(tier, '0%')
            cost_text = f'Coin: {cost} | Rate: {rate}'
            text_width = len(cost_text) * 10
            village.font.draw(cx - text_width // 2 + 20, y + h + 60, cost_text, (255, 255, 0))
        elif cost == 'MAX':
            village.font.draw(cx - 15, y + h + 60, 'MAX', (0, 255, 0))

    # 무기 선택 모드
    elif mode == 'weapon_select':
        tier = get_current_tier(name)
        icon_y = 300
        icon_size = 100

        if tier != 'none':
            is_selected = False
            if name == 'sword' and 'sword' in Player.current_weapon_id:
                is_selected = True
            elif name == 'arrow' and 'bow' in Player.current_weapon_id:
                is_selected = True

            tier_frame = 0
            if tier == 'silver':
                tier_frame = 1
            elif tier == 'gold':
                tier_frame = 2

            if name == 'sword' and village.icon_sword:
                village.icon_sword.clip_draw(tier_frame * 64, 0, 64, 64, cx + 150, icon_y, icon_size, icon_size)
            elif name == 'arrow' and village.icon_arrow:
                village.icon_arrow.clip_draw(tier_frame * 64, 0, 64, 64, cx + 150, icon_y, icon_size, icon_size)

            if is_selected:
                left = cx + 150 - icon_size // 2
                right = cx + 150 + icon_size // 2
                bottom = icon_y - icon_size // 2
                top = icon_y + icon_size // 2

                for i in range(3):
                    draw_rectangle(left - i, bottom - i, right + i, top + i)

            if name == 'sword':
                item_name = Player.player_sword_id.replace('_', ' ').upper()
            elif name == 'arrow':
                item_name = Player.player_bow_id.replace('_', ' ').upper()
            else:
                item_name = 'NONE'

            color = (0, 255, 0) if is_selected else (255, 255, 255)
            text_width = len(item_name) * 10
            village.font.draw(cx + 150 - text_width // 2, y + h + 20, item_name, color)
        else:
            # tier가 none인 경우 [None] 텍스트 표시
            village.font.draw(cx + 80, icon_y, '[None]', (150, 150, 150))

def handle_events():
    global running, enhance_active, weapon_select

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            if enhance_active or weapon_select:
                enhance_active = False # 강화 모드 비활성화
                weapon_select = False # 무기 선택 모드 비활성화
            else:
                game_framework.change_mode(title_mode)
        elif enhance_active or weapon_select:
            if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                mx = event.x
                my = get_canvas_height() - event.y

                # 메뉴 버튼 클릭 확인
                enhance_rect = MENU_BUTTONS.get('enhance')
                weapon_rect = MENU_BUTTONS.get('weapon')

                if enhance_rect and point_in_rect(mx, my, enhance_rect):
                    enhance_active = True
                    weapon_select = False
                elif weapon_rect and point_in_rect(mx, my, weapon_rect):
                    weapon_select = True
                    enhance_active = False
                elif enhance_active:
                    handle_enhance_click(mx, my)
                elif weapon_select:
                    handle_weapon_select_click(mx, my)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_f):
            if 480 <= common.player.x <= 590 and 370 <= common.player.y <= 380: # 던전 입구 좌표 범위
                game_framework.push_mode(dungeonmain_mode,(535, 60))
            elif 210 <= common.player.x <= 260 and 190 <= common.player.y <= 210:  # 짐 좌표 범위 - 아이템 강화
                enhance_active = True # 강화 모드 활성화
        else:
            common.player.handle_event(event)

def draw_enhance_ui():
    village.black_screen.clip_draw(5 * 768, 0, 768, 144, 512, 288, 1024, 576)

    # 메뉴 버튼 항상 표시
    for name, rect in MENU_BUTTONS.items():
        x, y, w, h = rect
        cx = x + w // 2
        cy = y + h // 2

        if name == 'enhance':
            frame = 0 if enhance_active else 1
            village.button_enhance.clip_draw(frame * 192, 0, 192, 192, cx, cy, w, h)
        elif name == 'weapon':
            frame = 0 if weapon_select else 1
            village.button_weapon.clip_draw(frame * 192, 0, 192, 192, cx, cy, w, h)

    # 강화 모드
    if enhance_active:
        village.font.draw(320, 50, 'Click the Start Button or Go to Game with ESC key', (200, 200, 200))
        for name, rect in BUTTONS.items():
            draw_button(name, rect)

        if coin_warning['active'] and village.info_coin:
            frame = coin_warning['frame']
            village.info_coin.clip_draw(0, frame * 78, 490, 78, 512, 288)

    # 무기 선택 모드
    elif weapon_select:
        village.font.draw(320, 50, 'Click the Item Image or Go to Game with ESC key', (200, 200, 200))
        for name in ['sword', 'arrow']:
            rect = BUTTONS.get(name)
            if rect:
                draw_button(name, rect, mode='weapon_select')

        # 무기 경고 표시
        if weapon_warning['active'] and village.info_weapon:
            frame = weapon_warning['frame']
            village.info_weapon.clip_draw(0, frame * 78, 490, 78, 512, 288)

        # 이미 선택된 무기 경고 표시
        if already_selected_warning['active'] and village.info_already_selected:
            frame = already_selected_warning['frame']
            village.info_already_selected.clip_draw(0, frame * 78, 490, 78, 512, 288)

def init(player_start_pos=None):
    global world
    global village
    global player
    global back_object
    global front_object
    global enhance_active
    global weapon_select
    global font

    enhance_active = False
    weapon_select = False
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
    elif weapon_select:
        update_weapon_warning()
        update_already_selected_warning()
    else:
        game_world.update()

def draw():
    clear_canvas()
    game_world.render()

    # 강화 UI 오버레이
    if enhance_active or weapon_select:
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
