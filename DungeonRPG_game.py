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

class Player:
    def __init__(self):
        self.walk_image = load_image('player_none_none_walk.png')
        self.idle_image = load_image('player_none_none_idle.png')
        self.dead_image = load_image('player_none_none_dead.png')

        self.x = 512
        self.y = 288
        self.frame = 0
        self.dx = 0
        self.dy = 0
        self.direction = 'down'

        self.is_attacking = False  # 공격 상태
        self.attack_start_time = 0  # 공격 시작 시간
        self.hp = 100  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

    def draw(self):
        direction_map = {
            'up': 3,
            'left': 2,
            'down': 1,
            'right': 0
        }
        row = direction_map[self.direction]
        offset_x = 0  # 중심 보정용 변수

        if not self.is_alive:
            # 죽은 상태 - dead 이미지 사용
            self.dead_image.clip_draw(0, 0, 64, 64, self.x, self.y)

        elif self.is_attacking:
            pass

        elif self.dx == 0 and self.dy == 0:
            # 정지 상태 - idle 이미지 사용
            self.idle_image.clip_draw(self.frame * 64, 64 * row, 64, 64, self.x, self.y)

        else:
            if self.direction == 'left':
                offset_x = -10
            elif self.direction == 'right':
                offset_x = +10
            elif self.direction == 'up':
                offset_x = +10
            elif self.direction == 'down':
                offset_x = +10

            self.walk_image.clip_draw(self.frame * 64, 64 * row, 64, 64,
                                        self.x + offset_x, self.y)

    def update(self):
        if self.dx == 0 and self.dy == 0 and self.is_attacking == False:  # 멈춰있는 상태
            self.frame = (self.frame + 1) % 2
        elif self.is_attacking:
            pass
        else:
            self.frame = (self.frame + 1) % 9
        self.x += self.dx
        self.y += self.dy

    def set_direction(self, dx, dy, direction):
        self.dx = dx
        self.dy = dy
        self.direction = direction

    def attack(self):
        if not self.is_attacking:  # 이미 공격 중이 아니면
            self.is_attacking = True
            self.attack_start_time = time.time()  # 공격 시작 시간 기록

    def damage(self):
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
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_w:
                player.set_direction(0, 5, 'up')
            elif event.key == SDLK_s:
                player.set_direction(0, -5, 'down')
            elif event.key == SDLK_a:
                player.set_direction(-5, 0, 'left')
            elif event.key == SDLK_d:
                player.set_direction(5, 0, 'right')
            elif event.key == SDLK_SPACE:  # 공격 키 처리
                player.attack()
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_w, SDLK_s, SDLK_a, SDLK_d):
                player.set_direction(0, 0, player.direction)

def reset_world():
    global running
    global world
    global background
    global player

    world = []
    running = True

    background = Background_Resource()
    world.append(background)

    player = Player()
    world.append(player)

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