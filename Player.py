import time

from pico2d import load_image


class Player:
    def __init__(self):
        self.walk_image = load_image('player_none_none_walk.png')
        self.idle_image = load_image('player_none_none_idle.png')
        self.dead_image = load_image('player_none_none_dead.png')

        self.x = 510
        self.y = 160

        self.frame = 0
        self.idle_frame_counter = 0  # idle 애니메이션용 카운터
        self.idle_frame_delay = 10  # 10프레임마다 idle 프레임 변경

        self.dx = 0
        self.dy = 0
        self.direction = 'down'

        # 마을의 4개 통로 영역
        self.village_paths = [
            {'min_x': 10, 'max_x': 1014, 'min_y': 150, 'max_y': 200},  # 중앙 메인 통로 - 1구역 - 전체 해당 부분
            {'min_x': 10, 'max_x': 155, 'min_y': 140, 'max_y': 200},  # 중앙 메인 통로 - 2구역 - 좌측 돌부리 부분
            {'min_x': 645, 'max_x': 1014, 'min_y': 140, 'max_y': 200},  # 중앙 메인 통로 - 3구역 - 우측 표지판 이후 부분
            {'min_x': 155, 'max_x': 225, 'min_y': 150, 'max_y': 200},  # 중앙 메인 통로 - 4구역 - 좌측 돌부리 옆 일부 풀밭 부분
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
            self.dead_image.clip_draw(0, 0, 64, 64, self.x, self.y, 100, 100)

        elif self.is_attacking:
            pass

        elif self.dx == 0 and self.dy == 0:
            # 정지 상태 - idle 이미지 사용
            self.idle_image.clip_draw(self.frame * 64, 64 * row, 64, 64, self.x, self.y, 100, 100)

        else:
            self.walk_image.clip_draw(self.frame * 64, 64 * row, 64, 64,
                                        self.x + offset_x, self.y, 100, 100)

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
