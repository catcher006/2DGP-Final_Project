import player
import game_world
from pico2d import *

class Player_Sword():
    def __init__(self):
        global player
        self.x = getattr(player, 'player_x', 0)
        self.y = getattr(player, 'player_y', 0)
        self.frame = getattr(player, 'player_frame', 0)

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x + 10, self.y - 40, self.x + 40, self.y - 15

    def update(self):
        self.x = getattr(player, 'player_x', self.x)
        self.y = getattr(player, 'player_y', self.y)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass