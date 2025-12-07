import game_framework
from pico2d import *
import title_mode

image = None
bgm = None
logo_start_time = 0.0

def init():
    global image, running, logo_start_time, bgm

    image = load_image('./image/background/logo_credit.png')
    bgm = load_wav('./sound/bgm/intro_bgm.wav')
    logo_start_time = get_time()
    bgm.set_volume(64)
    bgm.play()

    from game_data import GameData
    from ui import Ui
    GameData.initialize()
    GameData.apply_weapon()
    GameData.apply_player()
    Ui.coin = GameData.player_data['coins']
    Ui.hp = GameData.player_data['hp']

def finish():
    global image
    del image

def update():
    # Logo 모드가 7초 동안 지속되도록 설정
    global logo_start_time

    if get_time() - logo_start_time > 7.0:
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 1024, 576)
    update_canvas()

def handle_events():
    # 없는데도 받는 이유는 받지 않으면 쌓여서 queue overflow 발생
    # flush input
    events = get_events()

def pause():
    pass

def resume():
    pass