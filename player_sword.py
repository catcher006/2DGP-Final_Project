import player
import game_world
from pico2d import *

class Player_Sword():
    def __init__(self):
        global player
        self.x = getattr(player, 'player_x', 0)
        self.y = getattr(player, 'player_y', 0)

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def update(self):
        self.x = getattr(player, 'player_x', self.x)
        self.y = getattr(player, 'player_y', self.y)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass