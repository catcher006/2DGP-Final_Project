import goblin_boss
import game_world
import sounds
from pico2d import *

import sounds


class Goblin_Boss_Sword():
    def __init__(self, goblin_boss):
        self.goblin_boss = goblin_boss
        self.x = getattr(goblin_boss, 'x')
        self.y = getattr(goblin_boss, 'y')
        self.frame = int(getattr(goblin_boss, 'frame'))
        self.face_dir = int(getattr(goblin_boss, 'face_dir'))
        self.sound_played = False

        if sounds.lazer_sword and not self.sound_played:
            sounds.lazer_sword.play()
            self.sound_played = True

    def draw(self):
        # bb = self.get_bb()
        # if bb:
        #     draw_rectangle(*bb)
        pass

    def get_bb(self):
        f = int(self.frame)
        d = int(self.face_dir)

        if f > 5:
            return None

        if d == 0:
            if f == 0: return self.x + 26, self.y - 100, self.x + 138, self.y - 38 # frame : 0
            elif f == 1: return self.x + 16, self.y - 64, self.x + 50, self.y - 38  # frame : 1
            elif f == 2: return self.x - 70, self.y - 50, self.x + 24, self.y - 10  # frame : 2
            elif f == 3: return self.x - 98, self.y - 44, self.x + 54, self.y - 4  # frame : 3
            elif f == 4: return self.x + 44, self.y - 44, self.x + 252, self.y + 34  # frame : 4
            else: return self.x + 56, self.y + 6, self.x + 248, self.y + 34  # frame : 5

        elif d == 1:
            if f == 0: return self.x - 76, self.y - 104, self.x + 34, self.y - 42 # frame : 0
            elif f == 1: return self.x - 104, self.y - 54, self.x + 16, self.y - 38  # frame : 1
            elif f == 2: return self.x - 100, self.y - 50, self.x - 12, self.y + 36  # frame : 2
            elif f == 3: return self.x - 124, self.y - 66, self.x + 18, self.y + 32  # frame : 3
            elif f == 4: return self.x - 134, self.y - 154, self.x + 120, self.y - 34  # frame : 4
            else: return self.x - 18, self.y - 146, self.x + 198, self.y - 18  # frame : 5

        elif d == 2:
            if f == 0: return self.x - 138, self.y - 100, self.x - 26, self.y - 38 # frame : 0
            elif f == 1: return self.x - 50, self.y - 64, self.x - 16, self.y - 38  # frame : 1
            elif f == 2: return self.x - 24, self.y - 50, self.x + 70, self.y - 10  # frame : 2
            elif f == 3: return self.x - 54, self.y - 44, self.x + 98, self.y - 4  # frame : 3
            elif f == 4: return self.x - 252, self.y - 44, self.x - 44, self.y + 34  # frame : 4
            else: return self.x - 248, self.y + 6, self.x - 56, self.y + 34  # frame : 5

        elif d == 3:
            if f == 0: return self.x - 76, self.y - 54, self.x + 34, self.y + 8 # frame : 0
            elif f == 1: return self.x - 104, self.y - 48, self.x + 16, self.y - 32  # frame : 1
            elif f == 2: return self.x - 100, self.y - 80, self.x - 12, self.y + 6  # frame : 2
            elif f == 3: return self.x - 134, self.y - 74, self.x + 8, self.y + 24  # frame : 3
            elif f == 4: return self.x - 134, self.y - 8, self.x + 120, self.y + 112  # frame : 4
            else: return self.x - 18, self.y - 24, self.x + 198, self.y + 102  # frame : 5

        return None



    def update(self):
        # 좀비 객체에서 직접 값을 가져옴
        self.x = self.goblin_boss.x
        self.y = self.goblin_boss.y
        self.frame = int(self.goblin_boss.frame)
        self.face_dir = int(self.goblin_boss.face_dir)

        # 공격 프레임이 끝나거나 좀비가 공격 중이 아니거나 죽었으면 제거
        is_attacking = self.goblin_boss.is_attacking
        is_alive = self.goblin_boss.is_alive

        if self.frame >= 6 or not is_attacking or not is_alive:
            game_world.remove_object(self)

    def do(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass