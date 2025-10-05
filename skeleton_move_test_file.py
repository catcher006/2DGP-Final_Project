from pico2d import *
import random, time

class Skeleton_Mob:
    def __init__(self):
        self.walk_image = load_image('skeleton_mace_walk_all.png')
        self.attack_image = load_image('skeleton_mace_attack_all.png')  # 공격 이미지 추가
        self.dead_image = load_image('skeleton_mace_dead.png')  # 사망 이미지 추가

        self.x = 400
        self.y = 90
        self.frame = 0
        self.dx = 0
        self.dy = 0
        self.direction = 'down'

        self.mob_is_attacking = False  # 공격 상태
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

        if self.mob_is_attacking:
            # 공격 프레임은 프레임당 폭이 약간 넓으므로 중심 보정
            frame_width = 75 if self.direction == 'down' else 64
            if self.direction == 'left':
                offset_x = -10
            elif self.direction == 'right':
                offset_x = +10
            elif self.direction == 'up':
                offset_x = +10
            elif self.direction == 'down':
                offset_x = +10

            self.attack_image.clip_draw(self.frame * frame_width, 64 * row, frame_width, 64,
                                        self.x + offset_x, self.y)
        else:
            self.walk_image.clip_draw(self.frame * 64, 64 * row, 64, 64, self.x, self.y)

    def update(self):
        if self.dx == 0 and self.dy == 0 and self.mob_is_attacking == False:  # 멈춰있는 상태
            self.frame = 0  # 0열 고정
        elif self.mob_is_attacking:
            self.frame = (self.frame + 1) % 6  # 공격은 6프레임
            if time.time() - self.attack_start_time > 0.5:  # 공격 상태 해제 (0.5초 후)
                self.mob_is_attacking = False
        else:
            self.frame = (self.frame + 1) % 8  # 걷기는 8프레임
        self.x += self.dx
        self.y += self.dy

    def set_direction(self, dx, dy, direction):
        self.dx = dx
        self.dy = dy
        self.direction = direction

    def attack(self):
        if not self.mob_is_attacking:  # 이미 공격 중이 아니면
            self.mob_is_attacking = True
            self.attack_start_time = time.time()  # 공격 시작 시간 기록

    def damage(self):
        pass

def handle_events():
    global running
    global skeleton_mob  # 제어할 스켈레톤 객체
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_w:
                skeleton_mob.set_direction(0, 5, 'up')
            elif event.key == SDLK_s:
                skeleton_mob.set_direction(0, -5, 'down')
            elif event.key == SDLK_a:
                skeleton_mob.set_direction(-5, 0, 'left')
            elif event.key == SDLK_d:
                skeleton_mob.set_direction(5, 0, 'right')
            elif event.key == SDLK_SPACE:  # 공격 키 처리
                skeleton_mob.attack()
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_w, SDLK_s, SDLK_a, SDLK_d):
                skeleton_mob.set_direction(0, 0, skeleton_mob.direction)

open_canvas(1200,800)

def reset_world():
    global running
    global world # World List - 모든 객체를 갖고 있는 리스트
    global skeleton_mob

    world = [] # 하나도 객체가 없는 월드
    running = True

    skeleton_mob = Skeleton_Mob()  # skeleton_mob 객체 생성
    world.append(skeleton_mob)  # 월드에 추가

# 게임 로직
def update_world():
    for game_object in world:
        game_object.update()


def render_world():
    # 월드에 객체들을 그린다.
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
