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
        self.y = 144

        self.frame = 0
        self.idle_frame_counter = 0  # idle 애니메이션용 카운터
        self.idle_frame_delay = 10  # 10프레임마다 idle 프레임 변경

        self.dx = 0
        self.dy = 0
        self.direction = 'down'

        # 마을의 4개 통로 영역
        self.village_paths = [
            {'min_x': 10, 'max_x': 1014, 'min_y': 120, 'max_y': 200},  # 중앙 메인 통로
            {'min_x': 370, 'max_x': 520, 'min_y': 60, 'max_y': 120},  # 하단 중앙 통로
            {'min_x': 150, 'max_x': 200, 'min_y': 200, 'max_y': 250},  # 상단 죄측 통로
            {'min_x': 710, 'max_x': 735, 'min_y': 200, 'max_y': 250},  # 상단 우측 통로
        ]

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
            self.walk_image.clip_draw(self.frame * 64, 64 * row, 64, 64,
                                        self.x + offset_x, self.y)

    def update(self):
        if self.dx == 0 and self.dy == 0 and self.is_attacking == False:  # 멈춰있는 상태
            self.idle_frame_counter += 1
            if self.idle_frame_counter >= self.idle_frame_delay:
                self.frame = (self.frame + 1) % 2
                self.idle_frame_counter = 0

        elif self.is_attacking:
            pass

        else:
            self.frame = (self.frame + 1) % 9

            # 새로운 위치 계산
            new_x = self.x + self.dx
            new_y = self.y + self.dy

            # 4개 통로 영역 중 하나라도 포함되면 이동 허용
            can_move = False
            for path in self.village_paths:
                if (path['min_x'] <= new_x <= path['max_x'] and
                        path['min_y'] <= new_y <= path['max_y']):
                    can_move = True
                    break

            if can_move:
                self.x = new_x
                self.y = new_y

    def set_direction(self, dx, dy, direction):
        # 이동에서 정지로 바뀔 때 idle 프레임 즉시 시작
        if self.dx != 0 or self.dy != 0:  # 이전에 이동 중이었다면
            if dx == 0 and dy == 0:  # 지금 정지 상태가 되면
                self.frame = 0  # idle 첫 번째 프레임으로 설정
                self.idle_frame_counter = 0  # 카운터 리셋

        self.dx = dx
        self.dy = dy
        self.direction = direction
        print(f"x={self.x}, y={self.y}")

    def attack(self):
        if not self.is_attacking:  # 이미 공격 중이 아니면
            self.is_attacking = True
            self.attack_start_time = time.time()  # 공격 시작 시간 기록

    def damage(self):
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