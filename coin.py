from pico2d import load_image, draw_rectangle
import game_framework

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
        if group == 'player:coin':
            pass