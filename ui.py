from pico2d import *
import player
import settings


class Ui:
    coin = 1000000 # 최대값 9999999
    hp = 100
    paused = False

    sound_button = True
    tutorial_button = False
    information_button = False

    def __init__(self):
        self.pixel_font_25 = load_font('./font/PixelPurl.TTF', 25)
        self.pixel_font_20 = load_font('./font/PixelPurl.TTF', 20)
        self.hp_image = load_image('./image/ui/player/player_hp.png')
        self.ui_coin_image = load_image('./image/ui/item/coin.png')
        self.pause_button_image = load_image('./image/ui/button/pause_button.png')
        self.action_button_image = load_image('./image/ui/button/action_button.png')
        self.black_screen = load_image('./image/background/black_screen.png')
        self.setting_main_screen = load_image('./image/background/setting_main_screen.png')
        self.information_button_image = load_image('./image/ui/button/setting_information_button.png')

        # 사운드 설정
        self.sound_button_image = load_image('./image/ui/button/setting_sound_button.png')
        self.tutorial_button_image = load_image('./image/ui/button/setting_tutorial_button.png')
        self.sound_bar_image = load_image('./image/ui/button/sound_bar.png')
        self.sound_track_on_image = load_image('./image/ui/button/sound_track_on.png')
        self.sound_track_off_image = load_image('./image/ui/button/sound_track_off.png')
        self.name_bgm_image = load_image('./image/ui/button/bgm_sound_track.png')
        self.name_effect_image = load_image('./image/ui/button/effect_sound_track.png')

        # 튜토리얼 설정
        self.info_tuturial_page1_image = load_image('./image/ui/information/tutorial_page1.png')
        self.info_tuturial_page2_image = load_image('./image/ui/information/tutorial_page2.png')
        self.info_tuturial_page3_image = load_image('./image/ui/information/tutorial_page3.png')

        self.current_tutorial_page = 1
    def draw(self):
        self.ui_coin_image.draw(60, 560)
        self.pixel_font_25.draw(70, 560, f'{Ui.coin:d}', (255, 255, 0))
        self.hp_image.clip_draw(0, int(Ui.hp) * 54, 400, 54, 150, 540, 240, 15)
        self.pixel_font_20.draw(140, 560, 'Player HP:', (255, 255, 255))
        self.pixel_font_25.draw(215, 560, f'{Ui.hp:d}', (255, 255, 255))

        if Ui.paused:
            self.black_screen.clip_draw(5 * 768, 0, 768, 144, 512, 288, 1024, 576)

            self.setting_main_screen.draw(512,288)

            sound_idx = 0 if Ui.sound_button else 1
            self.sound_button_image.clip_draw(0, sound_idx * 30, 80, 30, 220, 488)

            tutorial_idx = 0 if Ui.tutorial_button else 1
            self.tutorial_button_image.clip_draw(0, tutorial_idx * 30, 80, 30, 300, 488)

            info_idx = 0 if Ui.information_button else 1
            self.information_button_image.clip_draw(0, info_idx * 30, 80, 30, 380, 488)

            if Ui.sound_button:
                # 배경음
                self.sound_bar_image.draw(560, 350)
                self.name_bgm_image.draw(230, 390)

                draw_rectangle(315 - 10, 340 - 10, 315 + 10, 340 + 10)

                if settings.setting_bgm_sound != 0:
                    self.sound_track_on_image.draw(230, 340)
                else:
                    self.sound_track_off_image.draw(230, 340)

                # 효과음
                self.sound_bar_image.draw(560, 200)
                self.name_effect_image.draw(230, 245)

                if settings.setting_effect_sound != 0:
                    self.sound_track_on_image.draw(230, 195)
                else:
                    self.sound_track_off_image.draw(230, 195)
            elif Ui.tutorial_button:
                if self.current_tutorial_page == 1:
                    self.info_tuturial_page1_image.draw(512, 288)
                elif self.current_tutorial_page == 2:
                    self.info_tuturial_page2_image.draw(512, 288)
                elif self.current_tutorial_page == 3:
                    self.info_tuturial_page3_image.draw(512, 288)

            self.action_button_image.draw(990, 550, 40, 40)
        else:
            self.pause_button_image.draw(990, 550, 40, 40)
    def update(self):
        Ui.hp = player.player_hp
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass