import goblin_mob
import game_world
import sounds
from pico2d import *

class Goblin_Mace():
    def __init__(self, goblin):
        self.goblin = goblin
        self.x = getattr(goblin, 'x')
        self.y = getattr(goblin, 'y')
        self.frame = int(getattr(goblin, 'frame'))
        self.face_dir = int(getattr(goblin, 'face_dir'))
        self.sound_played = False

        if sounds.mace_attack and not self.sound_played:
            sounds.mace_attack.play()
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
            if f == 0: return self.x + 22, self.y - 42, self.x + 40, self.y - 26  # frame : 0
            elif f == 1: return self.x + 4, self.y - 32, self.x + 22, self.y - 14  # frame : 1
            elif f == 2: return self.x - 20, self.y - 32, self.x - 2, self.y - 14  # frame : 2
            elif f == 3: return self.x + 8, self.y - 26, self.x + 32, self.y - 8  # frame : 3
            elif f == 4: return self.x + 36, self.y - 10, self.x + 70, self.y + 12  # frame : 4
            else: return self.x + 34, self.y - 4, self.x + 52, self.y + 12  # frame : 5

        elif d == 1:
            if f == 0: return self.x - 10, self.y - 44, self.x + 10, self.y - 28  # frame : 0
            elif f == 1: return self.x - 26, self.y - 30, self.x - 10, self.y - 14  # frame : 1
            elif f == 2: return self.x - 44, self.y - 24, self.x - 26, self.y - 6  # frame : 2
            elif f == 3: return self.x - 26, self.y - 40, self.x - 8, self.y - 24  # frame : 3
            elif f == 4: return self.x + 26, self.y - 50, self.x + 58, self.y - 24  # frame : 4
            else: return self.x + 54, self.y - 28, self.x + 72, self.y - 12  # frame : 5

        elif d == 2:
            if f == 0: return self.x - 40, self.y - 42, self.x - 22, self.y - 26  # frame : 0
            elif f == 1: return self.x - 24, self.y - 32, self.x - 6, self.y - 14  # frame : 1
            elif f == 2: return self.x, self.y - 32, self.x + 18, self.y - 14  # frame : 2
            elif f == 3: return self.x - 34, self.y - 26, self.x - 10, self.y - 8  # frame : 3
            elif f == 4: return self.x - 70, self.y - 10, self.x - 36, self.y + 14  # frame : 4
            else: return self.x - 52, self.y - 4, self.x - 34, self.y + 14  # frame : 5

        elif d == 3:
            if f == 0: return self.x - 10, self.y - 44, self.x + 10, self.y - 28  # frame : 0
            elif f == 1: return self.x - 14, self.y - 32, self.x + 5, self.y - 15  # frame : 1
            elif f == 2: return self.x - 38, self.y - 20, self.x - 20, self.y - 2  # frame : 2
            elif f == 3: return self.x - 18, self.y - 8, self.x + 9, self.y + 16  # frame : 3
            elif f == 4: return self.x - 10, self.y + 4, self.x + 58, self.y + 34  # frame : 4
            else: return self.x + 38, self.y - 14, self.x + 66, self.y + 4  # frame : 5

        return None



    def update(self):
        # 좀비 객체에서 직접 값을 가져옴
        self.x = self.goblin.x
        self.y = self.goblin.y
        self.frame = int(self.goblin.frame)
        self.face_dir = int(self.goblin.face_dir)

        # 공격 프레임이 끝나거나 좀비가 공격 중이 아니거나 죽었으면 제거
        is_attacking = self.goblin.is_attacking
        is_alive = self.goblin.is_alive

        if self.frame >= 6 or not is_attacking or not is_alive:
            game_world.remove_object(self)

    def do(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass