from pico2d import *

class Ui:
    coin = 100
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 25)
    def draw(self):
        self.font.draw(20, 560, f'Coin: {Ui.coin:06d}', (255, 255, 0))
    def update(self):
        pass
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass