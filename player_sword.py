import player
import game_world
import common
from pico2d import *

class Player_Sword():

    sword_sound = None

    def __init__(self):
        self.x = common.player.x
        self.y = common.player.y
        self.frame = common.player.frame
        self.face_dir = common.player.face_dir
        self.sound_played = False

        if Player_Sword.sword_sound is None:
            Player_Sword.sword_sound = load_wav('./sound/player/sword_attack.wav')
            Player_Sword.sword_sound.set_volume(32)

        if Player_Sword.sword_sound and not self.sound_played:
            Player_Sword.sword_sound.play()
            self.sound_played = True

    def draw(self):
        bb = self.get_bb()
        if bb:
            draw_rectangle(*bb)

    def get_bb(self):
        f = int(self.frame)
        d = int(self.face_dir)

        if f > 12:
            return None

        if d == 0:
            if f == 0: return self.x - 68, self.y - 10, self.x - 40, self.y + 8  # frame : 0
            elif f == 1: return self.x - 68, self.y - 48, self.x + 30, self.y + 8  # frame : 1
            elif f == 2: return self.x + 12, self.y - 48, self.x + 83, self.y - 6  # frame : 2
            elif f == 3: return self.x - 25, self.y - 42, self.x + 83, self.y - 6  # frame : 3
            elif f == 4: return self.x - 25, self.y - 28, self.x + 50, self.y - 6  # frame : 4
            elif f == 5: return self.x - 25, self.y - 28, self.x + 25, self.y - 8  # frame : 5
            elif f == 6: return self.x + 15, self.y - 28, self.x + 38, self.y - 10  # frame : 6
            elif f == 7: return self.x - 30, self.y - 23, self.x + 15, self.y - 17  # frame : 7
            elif f == 8: return self.x - 30, self.y - 23, self.x + 35, self.y - 4  # frame : 8
            elif f == 9: return self.x + 5, self.y - 48, self.x + 83, self.y - 6  # frame : 9
            elif f == 10: return self.x - 52, self.y - 50, self.x + 55, self.y - 20  # frame : 10
            elif f == 11: return self.x - 52, self.y - 52, self.x + 25, self.y - 15  # frame : 11
            else: return self.x - 52, self.y - 34, self.x - 22, self.y - 12  # frame : 12

        elif d == 1:
            if f == 0: return self.x - 28, self.y + 5, self.x - 20, self.y + 42  # frame : 0
            elif f == 1: return self.x - 56, self.y - 23, self.x - 20, self.y + 36  # frame : 1
            elif f == 2: return self.x - 56, self.y - 48, self.x + 52, self.y - 18  # frame : 2
            elif f == 3: return self.x - 12, self.y - 48, self.x + 52, self.y - 8  # frame : 3
            elif f == 4: return self.x + 12, self.y - 34, self.x + 54, self.y - 8  # frame : 4
            elif f == 5: return self.x + 12, self.y - 25, self.x + 24, self.y - 10  # frame : 5
            elif f == 6: return self.x - 20, self.y - 30, self.x + 18, self.y - 14  # frame : 6
            elif f == 7: return self.x + 8, self.y - 30, self.x + 22, self.y - 12  # frame : 7
            elif f == 8: return self.x + 8, self.y - 40, self.x + 56, self.y - 12  # frame : 8
            elif f == 9: return self.x - 68, self.y - 56, self.x + 56, self.y - 12  # frame : 9
            elif f == 10: return self.x - 76, self.y - 56, self.x, self.y + 4  # frame : 10
            elif f == 11: return self.x - 76, self.y - 50, self.x - 30, self.y + 4  # frame : 11
            else: return self.x - 74, self.y - 10, self.x - 30, self.y + 4  # frame : 12

        elif d == 2:
            if f == 0: return self.x + 34, self.y - 10, self.x + 66, self.y + 8  # frame : 0
            elif f == 1: return self.x - 30, self.y - 46, self.x + 66, self.y + 8  # frame : 1
            elif f == 2: return self.x - 84, self.y - 48, self.x - 16, self.y - 6  # frame : 2
            elif f == 3: return self.x - 84, self.y - 42, self.x + 24, self.y - 6  # frame : 3
            elif f == 4: return self.x - 54, self.y - 28, self.x + 24, self.y - 6  # frame : 4
            elif f == 5: return self.x - 26, self.y - 28, self.x + 24, self.y - 10  # frame : 5
            elif f == 6: return self.x - 38, self.y - 28, self.x - 8, self.y - 10  # frame : 6
            elif f == 7: return self.x - 8, self.y - 22, self.x + 30, self.y - 18  # frame : 7
            elif f == 8: return self.x - 36, self.y - 22, self.x + 30, self.y - 6  # frame : 8
            elif f == 9: return self.x - 84, self.y - 48, self.x - 8, self.y - 6  # frame : 9
            elif f == 10: return self.x - 58, self.y - 52, self.x + 52, self.y - 18  # frame : 10
            elif f == 11: return self.x - 16, self.y - 52, self.x + 52, self.y - 18  # frame : 11
            else: return self.x + 26, self.y - 32, self.x + 52, self.y - 18  # frame : 12

        elif d == 3:
            if f == 0: return self.x + 14, self.y - 44, self.x + 32, self.y - 26  # frame : 0
            elif f == 1: return self.x + 24, self.y - 44, self.x + 60, self.y - 4  # frame : 1
            elif f == 2: return self.x - 44, self.y - 20, self.x + 60, self.y + 14  # frame : 2
            elif f == 3: return self.x - 48, self.y - 40, self.x, self.y + 14  # frame : 3
            elif f == 4: return self.x - 50, self.y - 40, self.x, self.y + 14  # frame : 4
            elif f == 5: return self.x - 38, self.y - 40, self.x - 20, self.y - 20  # frame : 5
            elif f == 6: return self.x - 24, self.y - 30, self.x + 24, self.y - 4  # frame : 6
            elif f == 7: return self.x - 22, self.y - 48, self.x - 16, self.y - 24  # frame : 7
            elif f == 8: return self.x - 52, self.y - 46, self.x - 22, self.y - 4  # frame : 8
            elif f == 9: return self.x - 48, self.y - 6, self.x + 44, self.y + 18  # frame : 9
            elif f == 10: return self.x - 28, self.y - 14, self.x + 78, self.y + 18  # frame : 10
            elif f == 11: return self.x + 32, self.y - 14, self.x + 78, self.y + 12  # frame : 11
            else: return self.x + 32, self.y - 14, self.x + 78, self.y - 8  # frame : 12

        return None



    def update(self):
        self.x = common.player.x
        self.y = common.player.y
        self.frame = common.player.frame
        self.face_dir = common.player.face_dir

        if not player.Player.is_attacking:
            game_world.remove_object(self)

    def do(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass