from pico2d import load_wav

normal_click_sound = None
warning_sound = None

def init_sounds():
    global normal_click_sound, warning_sound

    if normal_click_sound is None:
        normal_click_sound = load_wav('./sound/click/normal_click.wav')
        normal_click_sound.set_volume(32)

    if warning_sound is None:
        warning_sound = load_wav('./sound/click/warning.wav')
        warning_sound.set_volume(32)