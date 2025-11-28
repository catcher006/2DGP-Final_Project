import zombie_boss
import game_world
from pico2d import *

class Zombie_Boss_Waraxe():
    def __init__(self, zombie_boss):
        self.zombie_boss = zombie_boss
        self.x = getattr(zombie_boss, 'x')
        self.y = getattr(zombie_boss, 'y')
        self.frame = int(getattr(zombie_boss, 'frame'))
        self.face_dir = int(getattr(zombie_boss, 'face_dir'))

    def draw(self):
        bb = self.get_bb()
        if bb:
            draw_rectangle(*bb)

    def get_bb(self):
        f = int(self.frame)
        d = int(self.face_dir)

        if f > 5:
            return None

        if d == 0:
            if f == 0: return self.x + 16, self.y - 78, self.x + 68, self.y - 6 # frame : 0
            elif f == 1: return self.x, self.y - 76, self.x + 58, self.y - 34  # frame : 1
            elif f == 2: return self.x - 62, self.y - 84, self.x, self.y - 42  # frame : 2
            elif f == 3: return self.x - 50, self.y - 82, self.x + 124, self.y - 22  # frame : 3
            elif f == 4: return self.x + 40, self.y - 58, self.x + 138, self.y + 22  # frame : 4
            else: return self.x + 56, self.y - 58, self.x + 138, self.y + 46  # frame : 5

        elif d == 1:
            if f == 0: return self.x - 48, self.y - 72, self.x + 24, self.y # frame : 0
            elif f == 1: return self.x - 72, self.y - 72, self.x - 4, self.y  # frame : 1
            elif f == 2: return self.x - 94, self.y - 70, self.x - 28, self.y - 26  # frame : 2
            elif f == 3: return self.x - 92, self.y - 78, self.x - 8, self.y - 30  # frame : 3
            elif f == 4: return self.x - 68, self.y - 122, self.x + 140, self.y - 20  # frame : 4
            else: return self.x - 42, self.y - 110, self.x + 152, self.y + 8  # frame : 5

        elif d == 2:
            if f == 0: return self.x - 70, self.y - 78, self.x - 18, self.y - 6  # frame : 0
            elif f == 1: return self.x - 60, self.y - 76, self.x, self.y - 34  # frame : 1
            elif f == 2: return self.x, self.y - 84, self.x + 62, self.y - 42  # frame : 2
            elif f == 3: return self.x - 126, self.y - 82, self.x + 50, self.y - 22  # frame : 3
            elif f == 4: return self.x - 138, self.y - 58, self.x - 40, self.y + 22  # frame : 4
            else: return self.x - 138, self.y - 58, self.x - 56, self.y + 46  # frame : 5

        elif d == 3:
            if f == 0: return self.x - 60, self.y - 70, self.x + 12, self.y + 2  # frame : 0
            elif f == 1: return self.x - 72, self.y - 44, self.x - 4, self.y - 4  # frame : 1
            elif f == 2: return self.x - 92, self.y - 42, self.x - 28, self.y + 2  # frame : 2
            elif f == 3: return self.x - 70, self.y - 42, self.x - 8, self.y  # frame : 3
            elif f == 4: return self.x - 76, self.y - 66, self.x + 94, self.y + 78  # frame : 4
            else: return self.x - 22, self.y - 52, self.x + 150, self.y + 72  # frame : 5

        return None



    def update(self):
        # 좀비 객체에서 직접 값을 가져옴
        self.x = self.zombie_boss.x
        self.y = self.zombie_boss.y
        self.frame = int(self.zombie_boss.frame)
        self.face_dir = int(self.zombie_boss.face_dir)

        # 공격 프레임이 끝나거나 좀비가 공격 중이 아니거나 죽었으면 제거
        is_attacking = self.zombie_boss.is_attacking
        is_alive = self.zombie_boss.is_alive

        if self.frame >= 6 or not is_attacking or not is_alive:
            game_world.remove_object(self)

    def do(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass