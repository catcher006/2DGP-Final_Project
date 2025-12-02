from pico2d import *
import player

class Ui:
    coin = 100
    hp = 100
    def __init__(self):
        self.coin_font = load_font('./font/PixelPurl.TTF', 25)
        self.hp_font = load_font('./font/PixelPurl.TTF', 20)
        self.hp_image = load_image('./image/ui/player/player_hp.png')
        self.ui_coin_image = load_image('./image/ui/item/coin.png')
    def draw(self):
        self.ui_coin_image.draw(60, 560)
        self.coin_font.draw(70, 560, f'{Ui.coin:d}', (255, 255, 0))
        self.hp_image.clip_draw(0, int(Ui.hp) * 54, 400, 54, 150, 540, 240, 15)
        self.hp_font.draw(140, 560, f'Player HP: {Ui.hp:d}', (255, 255, 255))
    def update(self):
        Ui.hp = player.player_hp
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass