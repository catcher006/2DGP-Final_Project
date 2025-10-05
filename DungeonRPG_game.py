from pico2d import *
import random, time

class Slime_Mob:
    pass

class Slime_Boss:
    pass

class Skeleton_Mob:
    pass

class Skeleton_Boss:
    pass

class Goblin_Mob:
    pass

class Goblin_Boss:
    pass

class Background_Resource:
    def __init__(self):
        self.backgrounds = {
            'village': load_image('village.png'),
        }

        # 현재 장소
        self.current_location = 'village'


    def update(self):
        # 배경 업데이트 로직 (현재는 빈 메서드)
        pass

    def draw(self):
        if self.current_location in self.backgrounds:
            self.backgrounds[self.current_location].draw_to_origin(0, 0, 1024, 576)


class Item:
    pass

class UI:
    pass

open_canvas(1024,576)

def handle_events():
    pass

def reset_world():
    global running
    global world
    global background

    world = []
    running = True

    background = Background_Resource()
    world.append(background)

def update_world():
    for game_object in world:
        game_object.update()

def render_world():
    clear_canvas()

    for game_object in world:
        game_object.draw()

    update_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.07)

close_canvas()