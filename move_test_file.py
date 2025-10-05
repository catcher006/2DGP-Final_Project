from pico2d import *
import random, time

class Skeleton_Mob:
    def __init__(self):
        self.walk_image = load_image('skeleton_mace_walk_all.png')
        self.attack_image = load_image('skeleton_mace_attack_all.png')  # 공격 이미지 추가
        self.x = 400
        self.y = 90
        self.frame = 0
        self.dx = 0
        self.dy = 0
        self.direction = 'down'
        self.mob_is_attacking = False  # 공격 상태
        self.attack_start_time = 0  # 공격 시작 시간

    def draw(self):
        direction_map = {
            'up': 3,  # 위쪽 방향에 해당하는 이미지 행
            'left': 2,  # 왼쪽 방향에 해당하는 이미지 행
            'down': 1,  # 아래쪽 방향에 해당하는 이미지 행
            'right': 0  # 오른쪽 방향에 해당하는 이미지 행
        }
        row = direction_map[self.direction]
        if self.mob_is_attacking:
            if self.direction == 'down':
                self.attack_image.clip_draw(self.frame * 75, 64 * row, 75, 64, self.x, self.y)
            else:
                self.attack_image.clip_draw(self.frame * 64, 64 * row, 64, 64, self.x, self.y)
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
