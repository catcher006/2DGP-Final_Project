import game_framework
from pico2d import *
import village_mode
import sounds

image = None

def init():
    global image
    image = load_image('./image/background/main_title.png')

    sounds.init_bgm_sounds()
    sounds.init_effect_sounds()

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw_to_origin(0, 0, 1024, 576)
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