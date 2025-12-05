from pico2d import load_wav, load_music

normal_click_sound = None
warning_sound = None
village_bgm = None
dungeon_bgm = None
stage1_bgm = None
stage2_bgm = None
stage3_bgm = None

setting_bgm_sound = 4
setting_effect_sound = 4

def init_bgm_sounds():
    global village_bgm, dungeon_bgm, stage1_bgm, stage2_bgm, stage3_bgm

    sound = 0 if setting_bgm_sound == 0 else 2 ** setting_bgm_sound

    if village_bgm is None:
        village_bgm = load_music('./sound/bgm/village_bgm.mp3')
        village_bgm.set_volume(sound)

    if dungeon_bgm is None:
        dungeon_bgm = load_music('./sound/bgm/dungeon_bgm.mp3')
        dungeon_bgm.set_volume(sound)

    if stage1_bgm is None:
        stage1_bgm = load_music('./sound/bgm/stage1_bgm.mp3')
        stage1_bgm.set_volume(sound)

    if stage2_bgm is None:
        stage2_bgm = load_music('./sound/bgm/stage2_bgm.mp3')
        stage2_bgm.set_volume(sound)

    if stage3_bgm is None:
        stage3_bgm = load_music('./sound/bgm/stage3_bgm.mp3')
        stage3_bgm.set_volume(sound)

def init_effect_sounds():
    global normal_click_sound, warning_sound

    sound = 0 if setting_effect_sound == 0 else 2 ** setting_effect_sound

    if normal_click_sound is None:
        normal_click_sound = load_wav('./sound/click/normal_click.wav')
        normal_click_sound.set_volume(sound)

    if warning_sound is None:
        warning_sound = load_wav('./sound/click/warning.wav')
        warning_sound.set_volume(sound)


def apply_bgm_volume():
    volume = 0 if setting_bgm_sound == 0 else 2 ** setting_bgm_sound

    if village_bgm is not None:
        village_bgm.set_volume(volume)
    if dungeon_bgm is not None:
        dungeon_bgm.set_volume(volume)
    if stage1_bgm is not None:
        stage1_bgm.set_volume(volume)
    if stage2_bgm is not None:
        stage2_bgm.set_volume(volume)
    if stage3_bgm is not None:
        stage3_bgm.set_volume(volume)


def apply_effect_volume():
    volume = 0 if setting_effect_sound == 0 else 2 ** setting_effect_sound

    if normal_click_sound is not None:
        normal_click_sound.set_volume(volume)
    if warning_sound is not None:
        warning_sound.set_volume(volume)