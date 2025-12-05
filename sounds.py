from pico2d import load_wav, load_music

normal_click_sound = None
warning_sound = None
village_bgm = None
dungeon_bgm = None
stage1_bgm = None
stage2_bgm = None
stage3_bgm = None

coin_sound = None

slime_hurt_sound = None
zombie_hurt_sound = None
zombie_dead_sound = None
goblin_hurt_sound = None
goblin_dead_sound = None

player_hurt_high_sound = None
player_hurt_low_sound = None
player_dead_sound = None
sword_attack_sound = None
arrow_sound = None

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
    global normal_click_sound, warning_sound, coin_sound
    global slime_hurt_sound
    global zombie_hurt_sound, zombie_dead_sound
    global goblin_hurt_sound, goblin_dead_sound
    global player_hurt_high_sound, player_hurt_low_sound, player_dead_sound
    global sword_attack_sound, arrow_sound

    sound = 0 if setting_effect_sound == 0 else 2 ** setting_effect_sound

    if normal_click_sound is None:
        normal_click_sound = load_wav('./sound/click/normal_click.wav')
        normal_click_sound.set_volume(sound)

    if warning_sound is None:
        warning_sound = load_wav('./sound/click/warning.wav')
        warning_sound.set_volume(sound)

    if coin_sound is None:
        coin_sound = load_wav('./sound/item/coin.wav')
        coin_sound.set_volume(sound)

    if slime_hurt_sound is None:
        slime_hurt_sound = load_wav('./sound/mob/slime_hurt.wav')
        slime_hurt_sound.set_volume(sound)

    if zombie_hurt_sound is None:
        zombie_hurt_sound = load_wav('./sound/mob/zombie_hurt.wav')
        zombie_hurt_sound.set_volume(sound)

    if zombie_dead_sound is None:
        zombie_dead_sound = load_wav('./sound/mob/zombie_dead.wav')
        zombie_dead_sound.set_volume(sound)

    if goblin_hurt_sound is None:
        goblin_hurt_sound = load_wav('./sound/mob/goblin_hurt.wav')
        goblin_hurt_sound.set_volume(sound)

    if goblin_dead_sound is None:
        goblin_dead_sound = load_wav('./sound/mob/goblin_dead.wav')
        goblin_dead_sound.set_volume(sound)

    if player_hurt_high_sound is None:
        player_hurt_high_sound = load_wav('./sound/player/player_hurt_high.wav')
        player_hurt_high_sound.set_volume(sound)

    if player_hurt_low_sound is None:
        player_hurt_low_sound = load_wav('./sound/player/player_hurt_low.wav')
        player_hurt_low_sound.set_volume(sound)

    if player_dead_sound is None:
        player_dead_sound = load_wav('./sound/player/player_dead.wav')
        player_dead_sound.set_volume(sound)

    if sword_attack_sound is None:
        sword_attack_sound = load_wav('./sound/player/sword_attack.wav')
        sword_attack_sound.set_volume(sound)

    if arrow_sound is None:
        arrow_sound = load_wav('./sound/player/arrow_sound.wav')
        arrow_sound.set_volume(sound)


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
    if coin_sound is not None:
        coin_sound.set_volume(volume)
    if slime_hurt_sound is not None:
        slime_hurt_sound.set_volume(volume)
    if zombie_hurt_sound is not None:
        zombie_hurt_sound.set_volume(volume)
    if zombie_dead_sound is not None:
        zombie_dead_sound.set_volume(volume)
    if goblin_hurt_sound is not None:
        goblin_hurt_sound.set_volume(volume)
    if goblin_dead_sound is not None:
        goblin_dead_sound.set_volume(volume)
    if player_hurt_high_sound is not None:
        player_hurt_high_sound.set_volume(volume)
    if player_hurt_low_sound is not None:
        player_hurt_low_sound.set_volume(volume)
    if player_dead_sound is not None:
        player_dead_sound.set_volume(volume)
    if sword_attack_sound is not None:
        sword_attack_sound.set_volume(volume)
    if arrow_sound is not None:
        arrow_sound.set_volume(volume)