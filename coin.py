from pico2d import load_image
import game_framework

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

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
    def update(self):
        self.frame = (int(self.frame) + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6