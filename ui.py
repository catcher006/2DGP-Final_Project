from pico2d import *
import player
import sounds


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
        self.current_bgm_sound = load_image('./image/ui/button/current_bgm_sound.png')
        self.want_bgm_sound = load_image('./image/ui/button/want_bgm_sound.png')
        self.current_effect_sound = load_image('./image/ui/button/current_effect_sound.png')
        self.want_effect_sound = load_image('./image/ui/button/want_effect_sound.png')

        # 튜토리얼 설정
        self.info_tuturial_page1_image = load_image('./image/ui/information/tutorial_page1.png')
        self.info_tuturial_page2_image = load_image('./image/ui/information/tutorial_page2.png')
        self.info_tuturial_page3_image = load_image('./image/ui/information/tutorial_page3.png')

        self.current_tutorial_page = 1
        self.hovered_bgm = -1
        self.hovered_effect = -1

        # 게임 정보 설정
        self.game_info_image = load_image('./image/ui/information/game_info_page.png')
        self.scroll_offset = 0
        self.max_scroll = 0  # 이미지 높이에 따라 계산
        self.info_view_height = 350  # 보이는 영역 높이
        self.info_view_y = 288  # 중심 y 좌표
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

                self.current_bgm_sound.draw(315 + 70 * sounds.setting_bgm_sound, 340, 20, 20)

                if self.hovered_bgm >= 0 and self.hovered_bgm != sounds.setting_bgm_sound:
                    self.want_bgm_sound.draw(315 + 70 * self.hovered_bgm, 340, 20, 20)

                if sounds.setting_bgm_sound != 0:
                    self.sound_track_on_image.draw(230, 340)
                else:
                    self.sound_track_off_image.draw(230, 340)

                # 효과음
                self.sound_bar_image.draw(560, 200)
                self.name_effect_image.draw(230, 245)

                self.current_effect_sound.draw(315 + 70 * sounds.setting_effect_sound, 190, 20, 20)

                if self.hovered_effect >= 0 and self.hovered_effect != sounds.setting_effect_sound:
                    self.want_effect_sound.draw(315 + 70 * self.hovered_effect, 190, 20, 20)

                if sounds.setting_effect_sound != 0:
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
            elif Ui.information_button:
                    self.game_info_image.draw(512, 288)
            else:
                self.pause_button_image.draw(990, 550, 40, 40)

            self.action_button_image.draw(990, 550, 40, 40)
        else:
            self.pause_button_image.draw(990, 550, 40, 40)
    def update(self):
        Ui.hp = player.player_hp

    def handle_events(self, event):
        if not Ui.paused:
            return False

        if event.type == SDL_MOUSEMOTION:
            mx = event.x
            my = get_canvas_height() - event.y
            self.handle_mouse_motion(mx, my)
            return True

        elif event.type == SDL_MOUSEWHEEL:
            mx = event.x
            my = get_canvas_height() - event.y
            # 게임 정보 영역에서만 스크롤 처리
            if Ui.information_button and 180 <= mx <= 844 and 113 <= my <= 463:
                self.scroll_offset -= event.y * 20  # 스크롤 속도 조절
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                return True

        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            sounds.normal_click_sound.play()
            mx = event.x
            my = get_canvas_height() - event.y

            # 일시정지 버튼
            if 970 <= mx <= 1010 and 530 <= my <= 570:
                Ui.paused = False
                self.reset_ui_state()
                return True

            # 사운드 버튼
            if 180 <= mx <= 260 and 473 <= my <= 503:
                Ui.sound_button = True
                Ui.tutorial_button = False
                Ui.information_button = False
                return True

            # 튜토리얼 버튼
            if 260 <= mx <= 340 and 473 <= my <= 503:
                Ui.tutorial_button = True
                Ui.sound_button = False
                Ui.information_button = False
                return True

            # 게임 정보 버튼
            if 340 <= mx <= 420 and 473 <= my <= 503:
                Ui.information_button = True
                Ui.sound_button = False
                Ui.tutorial_button = False
                return True

            # 사운드 바 클릭
            if self.handle_mouse_click(mx, my):
                return True

            # 튜토리얼 페이지 전환
            if Ui.tutorial_button:
                if 595 <= mx <= 617 and 122 <= my <= 160:
                    if self.current_tutorial_page < 3:
                        self.current_tutorial_page += 1
                    return True
                elif 407 <= mx <= 429 and 122 <= my <= 160:
                    if self.current_tutorial_page > 1:
                        self.current_tutorial_page -= 1
                    return True

        return False

    def handle_mouse_motion(self, mx, my):
        if not Ui.paused or not Ui.sound_button:
            self.hovered_bgm = -1
            self.hovered_effect = -1
            return

        # 배경음 사운드 바 영역
        for i in range(8):
            bar_x = 315 + 70 * i
            if bar_x - 35 <= mx <= bar_x + 35 and 325 <= my <= 365:
                self.hovered_bgm = i
                self.hovered_effect = -1
                return

        # 효과음 사운드 바 영역
        for i in range(8):
            bar_x = 315 + 70 * i
            if bar_x - 35 <= mx <= bar_x + 35 and 175 <= my <= 215:
                self.hovered_effect = i
                self.hovered_bgm = -1
                return

        self.hovered_bgm = -1
        self.hovered_effect = -1

    def handle_mouse_click(self, mx, my):
        if not Ui.paused or not Ui.sound_button:
            return False

        # 배경음 사운드 바 클릭
        for i in range(8):
            bar_x = 315 + 70 * i
            if bar_x - 35 <= mx <= bar_x + 35 and 325 <= my <= 365:
                sounds.setting_bgm_sound = i
                sounds.init_bgm_sounds()
                sounds.apply_bgm_volume()
                return True

        # 효과음 사운드 바 클릭
        for i in range(8):
            bar_x = 315 + 70 * i
            if bar_x - 35 <= mx <= bar_x + 35 and 175 <= my <= 215:
                sounds.setting_effect_sound = i
                sounds.init_effect_sounds()
                sounds.apply_effect_volume()
                return True

        return False

    def reset_ui_state(self):
        self.current_tutorial_page = 1
        self.hovered_bgm = -1
        self.hovered_effect = -1
        self.scroll_offset = 0
        Ui.sound_button = True
        Ui.tutorial_button = False
        Ui.information_button = False

    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass