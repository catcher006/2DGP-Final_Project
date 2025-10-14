from pico2d import *
from Player import Player


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


class Background:
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

class Front_Object:
    def __init__(self):
        self.front_objects = {
            'village': load_image('village_objects.png')  # 표지판 이미지
        }

        # 현재 장소
        self.current_location = 'village'


    def update(self):
        # 배경 업데이트 로직 (현재는 빈 메서드)
        pass

    def draw(self):
        if self.current_location in self.front_objects:
            self.front_objects[self.current_location].draw_to_origin(0, 0, 1024, 576)

class Back_Object:
    def __init__(self):
        self.back_objects = {
            'village': load_image('village_home_door.png')  # 집 문 오브젝트 이미지
        }
        # 현재 장소
        self.current_location = 'village'


    def update(self):
        # 배경 업데이트 로직 (현재는 빈 메서드)
        pass

    def draw(self):
        if self.current_location in self.back_objects:
            self.back_objects[self.current_location].clip_draw(0 * 1024, 1024 * 0, 1024, 1024, 182, 262, 100, 80)

class Item:
    pass

class UI:
    pass

open_canvas(1024,576)

def handle_events():
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

            # Player의 상태 머신에 이벤트 전달
            player.handle_event(event)

def reset_world():
    global running
    global world
    global background
    global player
    global back_object
    global front_object

    world = []
    running = True

    background = Background()
    world.append(background)

    back_object = Back_Object()
    world.append(back_object)

    player = Player()
    world.append(player)

    front_object = Front_Object()
    world.append(front_object)

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