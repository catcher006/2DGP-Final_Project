from pico2d import *
import player

class Ui:
    coin = 100
    hp = 100
    def __init__(self):
        self.coin_font = load_font('ENCR10B.TTF', 25)
        self.hp_font = load_font('ENCR10B.TTF', 15)
        self.hp_image = load_image('./image/ui/player/player_hp.png')
    def draw(self):
        self.coin_font.draw(20, 560, f'Coin: {Ui.coin:06d}', (255, 255, 0))
        self.hp_image.clip_draw(0, int(Ui.hp) * 54, 400, 54, 150, 540, 240, 15)
        if Ui.hp >= 100:
            self.hp_font.draw(140, 540, f'{Ui.hp:02d}', (255, 255, 255))
        elif 50 < Ui.hp < 100:
            self.hp_font.draw(150, 540, f'{Ui.hp:02d}', (255, 255, 255))
        elif Ui.hp == 50:
            self.hp_font.draw(143, 540, f'{((Ui.hp % 100) // 10):d}', (255, 255, 255))
            self.hp_font.draw(150, 540, f'{Ui.hp % 10:d}', (255, 0, 255))
        else:
            self.hp_font.draw(150 - 6, 540, f'{Ui.hp:02d}', (255, 0, 255))
    def update(self):
        Ui.hp = player.player_hp
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass