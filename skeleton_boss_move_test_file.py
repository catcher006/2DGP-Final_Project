from pico2d import *
import random, time

class Skeleton_Boss:
    def __init__(self):
        self.walk_image = load_image('skeleton_boss_walk_all.png')
        self.attack_image = load_image('skeleton_boss_attack_all.png')
        self.dead_image = load_image('skeleton_boss_dead.png')

        self.x = 350
        self.y = 200
        self.frame = 0
        self.dx = 0
        self.dy = 0
        self.direction = 'down'

        self.mob_is_moving = False  # 공격 상태
        self.attack_start_time = 0  # 공격 시작 시간

        self.hp = 300  # 체력 추가
        self.is_alive = True  # 생존 상태 추가

        self.is_pattern_moving = False
        self.target_distance = 0
        self.moved_distance = 0

        self.is_pattern_active = False
        self.current_pattern_index = 0
        self.pattern_delay_timer = 0

        self.movement_patterns = []
        self.pattern_state = 'moving'  # 패턴 상태

    # 방향과 거리를 받아서 5씩 이동하는 함수
    def move_function(self, direction, distance):
        direction_map = {
            'up': (0, 5),
            'down': (0, -5),
            'left': (-5, 0),
            'right': (5, 0)
        }

        if direction in direction_map:
            dx, dy = direction_map[direction]
            self.target_distance = distance
            self.moved_distance = 0
            self.set_direction(dx, dy, direction)
            self.is_pattern_moving = True

    # 여러 이동 패턴을 순차적으로 실행하는 함수
    def execute_movement_patterns(self):
        self.movement_patterns = [
            ('up', 250),
            ('up', 250),
            ('down', 250),
            ('right', 250),
            ('up', 170),
            ('down', 170),
            ('down', 170),
            ('up', 170),
            ('right', 250),
            ('up', 250),
            ('down', 250),
            ('down', 250),
            ('up', 250),
            ('left', 250),
            ('down', 170),
            ('up', 170),
            ('up', 170),
            ('down', 170),
            ('left', 250),
            ('down', 250),
        ]
        self.current_pattern_index = 0
        self.pattern_delay_timer = 0
        self.is_pattern_active = True
        self.pattern_state = 'moving'

        # 첫 번째 패턴 시작
        if self.movement_patterns:
            direction, distance = self.movement_patterns[0]
            self.move_function(direction, distance)

    def draw(self):
        direction_map = {
            'up': 3,
            'left': 2,
            'down': 1,
            'right': 0
        }
        row = direction_map[self.direction]
        offset_x = 0  # 중심 보정용 변수
        offset_y = 0  # 중심 보정용 변수

        if self.mob_is_moving:

            if self.direction == 'left':
                if self.frame == 0:
                    offset_x = 0
                elif self.frame == 1:
                    offset_x = -5
                elif self.frame == 2:
                    offset_x = 5
                elif self.frame == 3:
                    offset_x = -28
                elif self.frame in (4, 5):
                    offset_x = -40
                offset_y = -27

            elif self.direction == 'right':
                if self.frame == 0:
                    offset_x = 0
                elif self.frame == 1:
                    offset_x = +5
                elif self.frame == 2:
                    offset_x = -5
                elif self.frame == 3:
                    offset_x = +28
                elif self.frame in (4, 5):
                    offset_x = +40
                offset_y = -27

            elif self.direction == 'up':
                if self.frame == 0:
                    offset_x = 10
                    offset_y = -27
                elif self.frame == 1:
                    offset_x = -3
                    offset_y = -27
                elif self.frame == 2:
                    offset_x = -15
                    offset_y = -27
                elif self.frame == 3:
                    offset_x = 0
                    offset_y = -27
                elif self.frame == 4:
                    offset_x = 0
                    offset_y = -17
                elif self.frame == 5:
                    offset_x = 40
                    offset_y = -17

            elif self.direction == 'down':
                if self.frame == 0:
                    offset_x = 22
                    offset_y = -27
                elif self.frame == 1:
                    offset_x = -5
                    offset_y = -27
                elif self.frame == 2:
                    offset_x = -20
                    offset_y = -27
                elif self.frame == 3:
                    offset_x = -10
                    offset_y = -27
                elif self.frame == 4:
                    offset_x = 25
                    offset_y = -37
                elif self.frame == 5:
                    offset_x = 40
                    offset_y = -32

            self.attack_image.clip_draw(self.frame * 66, 66 * row, 64, 64,
                                        self.x + offset_x, self.y + offset_y, 200, 200)
        else:
            self.walk_image.clip_draw(self.frame * 64, 64 * row, 64, 64, self.x, self.y, 200, 200)

    def update(self):
        # 패턴 이동 처리
        if self.is_pattern_moving and self.is_alive:
            self.moved_distance += 5
            if self.moved_distance >= self.target_distance:
                self.set_direction(0, 0, self.direction)
                self.is_pattern_moving = False
                self.pattern_state = 'attacking'
                self.attack()  # 이동 완료 후 공격 시작

        # 패턴 상태에 따른 처리
        if self.is_pattern_active and self.is_alive:
            if self.pattern_state == 'attacking' and not self.mob_is_moving:
                # 공격이 끝나면 대기 상태로 전환
                self.pattern_state = 'waiting'
                self.pattern_delay_timer = time.time()

            elif self.pattern_state == 'waiting':
                if time.time() - self.pattern_delay_timer > 0.5:  # 0.5초 대기
                    # 다음 패턴으로 이동
                    self.current_pattern_index = (self.current_pattern_index + 1) % len(self.movement_patterns)
                    direction, distance = self.movement_patterns[self.current_pattern_index]
                    self.move_function(direction, distance)
                    self.pattern_state = 'moving'

        # 기존 update 로직
        if self.dx == 0 and self.dy == 0 and self.mob_is_moving == False:
            self.frame = 0
        elif self.mob_is_moving:
            self.frame = (self.frame + 1) % 6
            if time.time() - self.attack_start_time > 0.5:
                self.mob_is_moving = False
        else:
            self.frame = (self.frame + 1) % 9

        self.x += self.dx
        self.y += self.dy

    def set_direction(self, dx, dy, direction):
        self.dx = dx
        self.dy = dy
        self.direction = direction

    def attack(self):
        if not self.mob_is_moving:  # 이미 공격 중이 아니면
            self.mob_is_moving = True
            self.attack_start_time = time.time()  # 공격 시작 시간 기록

    def damage(self):
        pass

open_canvas(1200,800)

def reset_world():
    global running
    global world # World List - 모든 객체를 갖고 있는 리스트
    global skeleton_boss

    world = [] # 하나도 객체가 없는 월드
    running = True

    skeleton_boss = Skeleton_Boss()  # skeleton_boss 객체 생성
    world.append(skeleton_boss)  # 월드에 추가

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
# 이동 패턴 시작
skeleton_boss.execute_movement_patterns()

while running:
    update_world()
    render_world()
    delay(0.07)

close_canvas()
