from pico2d import *

import dungeonmain_mode
import game_world
import game_framework
import title_mode
from village import Village
from village_front_object import Village_Front_Object
from player import Player
from ui import Ui
import player as player_module

enhance_active = False # 강화 모드 활성화 플래그
font = None

# 강화 시스템 설정
TIER_LIST = ['normal', 'silver', 'gold']
COSTS = {'normal': 100, 'silver': 500}

BUTTONS = {
    'sword': (150, 150, 150, 50),
    'arrow': (450, 150, 150, 50),
    'shield': (750, 150, 150, 50)
}

# 버튼 애니메이션 상태
button_animations = {
    'sword': {'frame': 0, 'animating': False, 'time': 0},
    'arrow': {'frame': 0, 'animating': False, 'time': 0},
    'shield': {'frame': 0, 'animating': False, 'time': 0}
}

BUTTON_FRAME_SEQUENCE = [0, 1, 2, 1, 0]
BUTTON_FRAME_TIME = 0.1

def point_in_rect(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def get_current_tier(item_name):
    if item_name == 'sword':
        if 'silver' in player_module.player_sword_id:
            return 'silver'
        elif 'gold' in player_module.player_sword_id:
            return 'gold'
        return 'normal'
    elif item_name == 'arrow':
        if 'silver' in player_module.player_bow_id:
            return 'silver'
        elif 'gold' in player_module.player_bow_id:
            return 'gold'
        return 'normal'
    elif item_name == 'shield':
        if 'silver' in player_module.player_plate_id:
            return 'silver'
        elif 'gold' in player_module.player_plate_id:
            return 'gold'
        return 'normal'
    return 'normal'


def start_button_animation(button_name):
    """버튼 애니메이션 시작"""
    button_animations[button_name]['animating'] = True
    button_animations[button_name]['time'] = 0
    button_animations[button_name]['sequence_index'] = 0


def update_button_animations():
    """버튼 애니메이션 업데이트"""
    for name, anim in button_animations.items():
        if anim['animating']:
            anim['time'] += game_framework.frame_time

            if anim['time'] >= BUTTON_FRAME_TIME:
                anim['time'] = 0
                anim['sequence_index'] += 1

                if anim['sequence_index'] >= len(BUTTON_FRAME_SEQUENCE):
                    anim['animating'] = False
                    anim['sequence_index'] = 0
                    anim['frame'] = 0
                else:
                    anim['frame'] = BUTTON_FRAME_SEQUENCE[anim['sequence_index']]


def handle_enhance_click(mx, my):
    """버튼 클릭 처리"""
    for name, rect in BUTTONS.items():
        if point_in_rect(mx, my, rect):
            print(f"Clicked {name} button!")
            start_button_animation(name)


def draw_button(name, rect):
    x, y, w, h = rect
    cx = x + w // 2
    cy = y + h // 2

    # 애니메이션 프레임 가져오기
    frame = button_animations[name]['frame']
    print(f"Drawing {name} button with frame {frame}")  # 디버그용

    village.button_start.clip_draw(320 * frame, 0, 320, 115, cx, cy, w, h)

    if font:
        tier = get_current_tier(name)
        cost = COSTS.get(tier, 'MAX')
        font.draw(x, y + h + 80, f'{name.upper()} [{tier.upper()}]', (255, 255, 255))
        if cost != 'MAX':
            font.draw(x + 30, y + h + 15, f'Cost: {cost}', (255, 255, 0))

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
            if 480 <= player.x <= 590 and 370 <= player.y <= 380: # 던전 입구 좌표 범위
                game_framework.push_mode(dungeonmain_mode,(535, 60))
            elif 210 <= player.x <= 260 and 190 <= player.y <= 210:  # 짐 좌표 범위 - 아이템 강화
                enhance_active = True # 강화 모드 활성화
        else:
            player.handle_event(event)

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

def handle_enhance_click(mx, my):
    """버튼 클릭 처리"""
    print(f"Checking click at ({mx}, {my})")
    for name, rect in BUTTONS.items():
        print(f"  Button '{name}': {rect}")
        if point_in_rect(mx, my, rect):
            print(f"  -> Clicked {name} button!")
            start_button_animation(name)
            return
    print("  -> No button clicked")

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

    player = Player()
    # 마을 모드에서 이동 검사 콜백을 마을 객체에 위임
    player.move_validator = village.is_walkable
    # 시작 좌표 설정
    if player_start_pos:
        player.x, player.y = player_start_pos
    else:
        player.x, player.y = 510, 160  # 기본 좌표
    game_world.add_object((player), 2)

    front_object = Village_Front_Object()
    game_world.add_object((front_object), 3)

    ui = Ui()
    game_world.add_object(ui, 4)

def update():
    if enhance_active:
        update_button_animations()
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

    if player_start_pos:
        player.x, player.y = player_start_pos

    game_world.add_object(village, 0)
    game_world.add_object(player, 2)
    game_world.add_object(front_object, 3)

    ui = Ui()
    game_world.add_object(ui, 4)
