import game_framework
from pico2d import *
import village_mode
import sounds

image = None
title_image = None
font = None

def init():
    global image, title_image, font
    image = load_image('./image/background/main_title.png')
    title_image = load_image('./image/background/title.png')
    font = load_font('./font/PixelPurl.TTF', 40)

    sounds.init_bgm_sounds()
    sounds.init_effect_sounds()

    sounds.title_sound.repeat_play()

def finish():
    global image, title_image, font

    sounds.title_sound.stop()

    if image:
        del image
    if title_image:
        del title_image
    if font:
        del font
    image = None
    title_image = None
    font = None

def update():
    pass

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 1024, 576)
    title_image.draw(512, 288)
    font.draw(80, 50, 'ESC key to end the game, click to start the game or space bar', (200, 200, 200))
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(village_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            sounds.normal_click_sound.play()
            game_framework.change_mode(village_mode)

def pause():
    pass

def resume():
    pass