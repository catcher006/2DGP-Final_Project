from pico2d import *
import player
import sounds


class Ui:
    coin = 100 # 최대값 9999999
    hp = 100
    paused = False
    game_over = False

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
        self.resource_info_images = []
        for i in range(1, 4):
            img = load_image(f'./image/ui/information/resource_info_{i}.png')
            self.resource_info_images.append(img)

        # 게임 오버 화면 추가
        self.game_over_screen = load_image('./image/ui/information/game_over.png')
        self.restart_button_image = load_image('./image/ui/button/restart_game_button.png')
        self.quit_button_image = load_image('./image/ui/button/quit_game_button.png')

        self.game_over_sound_played = False  # 게임 오버 사운드 재생 플래그
        self.hovered_restart = False
        self.hovered_quit = False

        self.scroll_offset = 0
        self.max_scroll = 0  # 이미지 높이에 따라 계산
        self.info_view_height = 350  # 보이는 영역 높이
        self.info_view_y = 288  # 중심 y 좌표

        # 마우스 위치 추적
        self.mouse_x = 0
        self.mouse_y = 0
    def draw(self):
        self.ui_coin_image.draw(60, 560)
        self.pixel_font_25.draw(70, 560, f'{Ui.coin:d}', (255, 255, 0))
        self.hp_image.clip_draw(0, int(Ui.hp) * 54, 400, 54, 150, 540, 240, 15)
        self.pixel_font_20.draw(140, 560, 'Player HP:', (255, 255, 255))
        self.pixel_font_25.draw(215, 560, f'{Ui.hp:d}', (255, 255, 255))

        # 게임 오버 화면
        if Ui.game_over:
            self.black_screen.clip_draw(5 * 768, 0, 768, 144, 512, 288, 1024, 576)
            self.game_over_screen.draw(512, 338)

            # 게임 오버 사운드를 한 번만 재생
            if not self.game_over_sound_played:
                sounds.game_over_sound.play(1)
                self.game_over_sound_played = True

            # 재시작 버튼 (호버 시 0번 인덱스)
            restart_idx = 0 if self.hovered_restart else 1
            self.restart_button_image.clip_draw(0, restart_idx * 60, 160, 60, 412, 150)

            # 종료 버튼 (호버 시 0번 인덱스)
            quit_idx = 0 if self.hovered_quit else 1
            self.quit_button_image.clip_draw(0, quit_idx * 60, 160, 60, 612, 150)

            return

        # 일시정지 화면
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

                if len(self.resource_info_images) > 0:
                    view_x = 562
                    view_y = 228
                    view_width = 550
                    view_height = 180

                    # 전체 콘텐츠 높이
                    total_height = sum(img.h for img in self.resource_info_images)

                    # 스크롤 가능한 최대 범위
                    self.max_scroll = 20938

                    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

                    # 보이는 영역의 상단/하단
                    view_top = view_y + view_height // 2
                    view_bottom = view_y - view_height // 2

                    # 콘텐츠 시작 위치: view_top에서 시작, scroll_offset만큼 위로 이동
                    content_y = view_top + self.scroll_offset

                    for img in self.resource_info_images:
                        img_height = img.h
                        img_top = content_y
                        img_bottom = content_y - img_height

                        # 화면과 겹치는지 확인
                        if img_bottom < view_top and img_top > view_bottom:
                            visible_top = min(img_top, view_top)
                            visible_bottom = max(img_bottom, view_bottom)
                            visible_height = visible_top - visible_bottom

                            clip_from_top = max(0, img_top - view_top)
                            clip_from_bottom = max(0, view_bottom - img_bottom)
                            clip_height = img_height - clip_from_top - clip_from_bottom

                            draw_y = (visible_top + visible_bottom) // 2

                            img.clip_draw(
                                0, clip_from_bottom,
                                view_width, clip_height,
                                view_x, draw_y,
                                view_width, visible_height
                            )

                        content_y -= img_height
            else:
                self.pause_button_image.draw(990, 550, 40, 40)

            self.action_button_image.draw(990, 550, 40, 40)
        else:
            self.pause_button_image.draw(990, 550, 40, 40)
    def update(self):
        Ui.hp = player.player_hp

    def handle_events(self, event):
        if Ui.game_over:

            if event.type == SDL_MOUSEMOTION:
                mx = event.x
                my = get_canvas_height() - event.y

                # 재시작 버튼
                if 332 <= mx <= 492 and 120 <= my <= 180:
                    self.hovered_restart = True
                    self.hovered_quit = False
                # 종료 버튼
                elif 532 <= mx <= 692 and 120 <= my <= 180:
                    self.hovered_quit = True
                    self.hovered_restart = False
                else:
                    self.hovered_restart = False
                    self.hovered_quit = False
                return True

            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                sounds.normal_click_sound.play()
                mx = event.x
                my = get_canvas_height() - event.y

                # 재시작 버튼 클릭
                if 332 <= mx <= 492 and 120 <= my <= 180:
                    self.restart_game()
                    return True

                # 종료 버튼 클릭
                if 532 <= mx <= 692 and 120 <= my <= 180:
                    self.quit_game()
                    return True

            return True

        if not Ui.paused:
            return False

        if event.type == SDL_MOUSEMOTION:
            self.mouse_x = event.x
            self.mouse_y = get_canvas_height() - event.y
            self.handle_mouse_motion(self.mouse_x, self.mouse_y)
            return True


        elif event.type == SDL_MOUSEWHEEL:
            # 게임 정보 영역에서만 스크롤 처리
            if Ui.information_button and 180 <= self.mouse_x <= 844 and 113 <= self.mouse_y <= 463:
                self.scroll_offset -= event.y * 20
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
        self.game_over_sound_played = False
        Ui.sound_button = True
        Ui.tutorial_button = False
        Ui.information_button = False

    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass

    def restart_game(self):
        """게임 재시작 - 모든 상태 초기화 후 타이틀로 이동"""
        import game_framework
        import game_world
        import title_mode
        from stage1_0 import Stage1_0
        from stage2_0 import Stage2_0
        from stage3_0 import Stage3_0

        # 게임 월드 완전 초기화
        game_world.clear()

        # UI 상태 초기화
        Ui.game_over = False
        Ui.paused = False
        Ui.hp = 100
        Ui.coin = 100
        self.game_over_sound_played = False
        self.reset_ui_state()

        # 플레이어 상태 초기화
        player.player_hp = 100
        player.Player.is_alive = True

        # 스테이지 플래그 초기화
        Stage1_0.stage1_0_create = False
        Stage2_0.stage2_0_create = False
        Stage3_0.stage3_0_create = False

        # 모든 모드 스택 제거하고 타이틀 모드로 변경
        game_framework.change_mode(title_mode)

    def quit_game(self):
        """게임 종료"""
        import game_framework
        game_framework.quit()