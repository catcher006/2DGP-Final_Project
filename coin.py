from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import stage1_0_mode, stage1_1_mode, stage1_2_mode, stage1_3_mode
import stage1_4_mode, stage1_5_mode, stage1_6_mode, stage1_7_mode
from stage1_0 import Stage1_0
from stage1_1 import Stage1_1
from stage1_2 import Stage1_2
from stage1_3 import Stage1_3
from stage1_4 import Stage1_4
from stage1_5 import Stage1_5
from stage1_6 import Stage1_6
from stage1_7 import Stage1_7
from ui import Ui

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Coin:
    def __init__(self):
        self.image = load_image("./image/item/coin.png")
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

            Ui.coin += 50
            game_world.remove_object(self)
            if Stage1_0.current_mode:
                stage1_0_mode.coins.remove(self)
            elif Stage1_1.current_mode:
                stage1_1_mode.coins.remove(self)
            elif Stage1_2.current_mode:
                stage1_2_mode.coins.remove(self)
            elif Stage1_3.current_mode:
                stage1_3_mode.coins.remove(self)
            elif Stage1_4.current_mode:
                stage1_4_mode.coins.remove(self)
            elif Stage1_5.current_mode:
                stage1_5_mode.coins.remove(self)
            elif Stage1_6.current_mode:
                stage1_6_mode.coins.remove(self)
            elif Stage1_7.current_mode:
                stage1_7_mode.coins.remove(self)

            print(f"After collection: {Ui.coin}")  # 디버그 출력