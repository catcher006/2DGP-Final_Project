from pico2d import load_image, draw_rectangle, load_wav
import game_framework
import game_world
import stage1_0_mode, stage1_1_mode, stage1_2_mode, stage1_3_mode
import stage1_4_mode, stage1_5_mode, stage1_6_mode, stage1_7_mode
import stage2_0_mode, stage2_1_mode, stage2_2_mode, stage2_3_mode
import stage2_4_mode, stage2_5_mode, stage2_6_mode, stage2_7_mode
import stage2_8_mode, stage2_9_mode, stage2_10_mode, stage2_11_mode
import stage3_0_mode, stage3_1_mode, stage3_2_mode, stage3_3_mode
import stage3_4_mode, stage3_5_mode, stage3_6_mode, stage3_7_mode
import stage3_8_mode, stage3_9_mode, stage3_10_mode, stage3_11_mode
from stage1_0 import Stage1_0
from stage1_1 import Stage1_1
from stage1_2 import Stage1_2
from stage1_3 import Stage1_3
from stage1_4 import Stage1_4
from stage1_5 import Stage1_5
from stage1_6 import Stage1_6
from stage1_7 import Stage1_7
from stage2_0 import Stage2_0
from stage2_1 import Stage2_1
from stage2_2 import Stage2_2
from stage2_3 import Stage2_3
from stage2_4 import Stage2_4
from stage2_5 import Stage2_5
from stage2_6 import Stage2_6
from stage2_7 import Stage2_7
from stage2_8 import Stage2_8
from stage2_9 import Stage2_9
from stage2_10 import Stage2_10
from stage2_11 import Stage2_11
from stage3_0 import Stage3_0
from stage3_1 import Stage3_1
from stage3_2 import Stage3_2
from stage3_3 import Stage3_3
from stage3_4 import Stage3_4
from stage3_5 import Stage3_5
from stage3_6 import Stage3_6
from stage3_7 import Stage3_7
from stage3_8 import Stage3_8
from stage3_9 import Stage3_9
from stage3_10 import Stage3_10
from stage3_11 import Stage3_11
from ui import Ui

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Coin:
    coin_sound = None

    def __init__(self):
        self.image = load_image("./image/item/coin.png")
        if not Coin.coin_sound:
            Coin.coin_sound = load_wav('./sound/item/coin.wav')
            Coin.coin_sound.set_volume(32)
        self.frame = 0
        self.x, self.y = 512, 288
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass
    def draw(self):
        self.image.clip_draw(int(self.frame) * 17,0, 17, 16, self.x, self.y, 32, 32)
        bb = self.get_bb()
        if bb:
            draw_rectangle(*bb)
    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
    def get_bb(self):
        frame_idx = int(self.frame)

        if frame_idx == 0:
            return self.x - 17, self.y - 16, self.x + 15, self.y + 15  # frame : 0
        elif frame_idx == 1:
            return self.x - 15, self.y - 16, self.x + 12, self.y + 15  # frame : 1
        elif frame_idx == 2:
            return self.x - 12, self.y - 16, self.x + 8, self.y + 15  # frame : 2
        elif frame_idx == 3:
            return self.x - 8, self.y - 16, self.x + 4, self.y + 15  # frame : 3
        elif frame_idx == 4:
            return self.x - 5, self.y - 16, self.x + 3, self.y + 15  # frame : 4
        elif frame_idx == 5:
            return self.x - 8, self.y - 16, self.x + 4, self.y + 15  # frame : 5
        elif frame_idx == 6:
            return self.x - 12, self.y - 16, self.x + 8, self.y + 15  # frame : 6
        elif frame_idx == 7:
            return self.x - 15, self.y - 16, self.x + 12, self.y + 15  # frame : 7
        return None

    def handle_collision(self, group, other):
        print(f"Collision detected! Group: {group}")  # 디버그 출력

        if group == 'player:coin':
            print(f"Coin collected! Current coins: {Ui.coin}")  # 디버그 출력

            if Ui.coin + 50 <= 99999999:
                Ui.coin += 50
            elif Ui.coin > 99999999 - 50:
                Ui.coin = 99999999

            if Coin.coin_sound:
                Coin.coin_sound.play()

            try:
                game_world.remove_object(self)
            except Exception as e:
                print(f"game_world.remove_object error: {e}")
            # 현재 활성화된 모드의 coins와 saved_coins에서 제거
            def remove_from_mode(mode, mode_module):
                if self in mode_module.coins:
                    mode_module.coins.remove(self)
                # saved_coins에서 좌표가 같은 코인 정보 제거
                if hasattr(mode, 'saved_coins'):
                    mode.saved_coins = [
                        c for c in mode.saved_coins
                        if not (c['x'] == self.x and c['y'] == self.y)
                    ]
            if Stage1_0.current_mode:
                remove_from_mode(Stage1_0, stage1_0_mode)
            elif Stage1_1.current_mode:
                remove_from_mode(Stage1_1, stage1_1_mode)
            elif Stage1_2.current_mode:
                remove_from_mode(Stage1_2, stage1_2_mode)
            elif Stage1_3.current_mode:
                remove_from_mode(Stage1_3, stage1_3_mode)
            elif Stage1_4.current_mode:
                remove_from_mode(Stage1_4, stage1_4_mode)
            elif Stage1_5.current_mode:
                remove_from_mode(Stage1_5, stage1_5_mode)
            elif Stage1_6.current_mode:
                remove_from_mode(Stage1_6, stage1_6_mode)
            elif Stage1_7.current_mode:
                remove_from_mode(Stage1_7, stage1_7_mode)
            elif Stage2_0.current_mode:
                remove_from_mode(Stage2_0, stage2_0_mode)
            elif Stage2_1.current_mode:
                remove_from_mode(Stage2_1, stage2_1_mode)
            elif Stage2_2.current_mode:
                remove_from_mode(Stage2_2, stage2_2_mode)
            elif Stage2_3.current_mode:
                remove_from_mode(Stage2_3, stage2_3_mode)
            elif Stage2_4.current_mode:
                remove_from_mode(Stage2_4, stage2_4_mode)
            elif Stage2_5.current_mode:
                remove_from_mode(Stage2_5, stage2_5_mode)
            elif Stage2_6.current_mode:
                remove_from_mode(Stage2_6, stage2_6_mode)
            elif Stage2_7.current_mode:
                remove_from_mode(Stage2_7, stage2_7_mode)
            elif Stage2_8.current_mode:
                remove_from_mode(Stage2_8, stage2_8_mode)
            elif Stage2_9.current_mode:
                remove_from_mode(Stage2_9, stage2_9_mode)
            elif Stage2_10.current_mode:
                remove_from_mode(Stage2_10, stage2_10_mode)
            elif Stage2_11.current_mode:
                remove_from_mode(Stage2_11, stage2_11_mode)
            elif Stage3_0.current_mode:
                remove_from_mode(Stage3_0, stage3_0_mode)
            elif Stage3_1.current_mode:
                remove_from_mode(Stage3_1, stage3_1_mode)
            elif Stage3_2.current_mode:
                remove_from_mode(Stage3_2, stage3_2_mode)
            elif Stage3_3.current_mode:
                remove_from_mode(Stage3_3, stage3_3_mode)
            elif Stage3_4.current_mode:
                remove_from_mode(Stage3_4, stage3_4_mode)
            elif Stage3_5.current_mode:
                remove_from_mode(Stage3_5, stage3_5_mode)
            elif Stage3_6.current_mode:
                remove_from_mode(Stage3_6, stage3_6_mode)
            elif Stage3_7.current_mode:
                remove_from_mode(Stage3_7, stage3_7_mode)
            elif Stage3_8.current_mode:
                remove_from_mode(Stage3_8, stage3_8_mode)
            elif Stage3_9.current_mode:
                remove_from_mode(Stage3_9, stage3_9_mode)
            elif Stage3_10.current_mode:
                remove_from_mode(Stage3_10, stage3_10_mode)
            elif Stage3_11.current_mode:
                remove_from_mode(Stage3_11, stage3_11_mode)

            print(f"After collection: {Ui.coin}")  # 디버그 출력