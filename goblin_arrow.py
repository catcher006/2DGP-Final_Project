from pico2d import *
import game_framework
import game_world
import goblin_mob
import math

# Arrow Speed
PIXEL_PER_METER = (10.0 / 0.3)
ARROW_SPEED_KMPH = 60.0
ARROW_SPEED_MPM = (ARROW_SPEED_KMPH * 1000.0 / 60.0)
ARROW_SPEED_MPS = (ARROW_SPEED_MPM / 60.0)
ARROW_SPEED_PPS = (ARROW_SPEED_MPS * PIXEL_PER_METER)


class Goblin_Arrow:
    image = None

    def __init__(self, goblin):
        if Goblin_Arrow.image is None:
            Goblin_Arrow.image = load_image('./image/item/arrow.png')

        self.goblin = goblin
        self.x = getattr(goblin, 'x')
        self.y = getattr(goblin, 'y')
        self.frame = int(getattr(goblin, 'frame'))
        self.face_dir = int(getattr(goblin, 'face_dir'))

        self.is_fired = False  # 발사 여부
        self.speed = ARROW_SPEED_PPS
        self.distance_traveled = 0
        self.max_distance = 250  # 최대 비행 거리

        self.is_removed = False  # 제거 플래그

        # 방향별 이동 벡터
        self.direction_vectors = {
            0: (1, 0),  # 오른쪽
            1: (0, -1),  # 아래
            2: (-1, 0),  # 왼쪽
            3: (0, 1)  # 위
        }

    def update(self):
        self.frame = int(self.goblin.frame)

        # 발사 전: 플레이어를 따라다님
        if not self.is_fired:
            self.x = self.goblin.x
            self.y = self.goblin.y
            self.face_dir = int(self.goblin.face_dir)

            # 프레임 7에서 발사
            if self.frame >= 9:
                self.is_fired = True

        # 발사 후: 날아감
        else:
            dx, dy = self.direction_vectors[self.face_dir]
            move_distance = self.speed * game_framework.frame_time

            self.x += dx * move_distance
            self.y += dy * move_distance
            self.distance_traveled += move_distance

            # 최대 거리를 넘거나 화면 밖으로 나가면 제거
            if self.distance_traveled >= self.max_distance or \
                    self.x < 85 or self.x > 990 or self.y < 60 or self.y > 540:
                game_world.remove_object(self)

        # 공격이 끝나면 (프레임 13) 아직 발사 안됐으면 제거
        is_attacking = self.goblin.is_attacking
        is_alive = self.goblin.is_alive

        if self.frame >= 13 or not is_attacking or not is_alive:
            if not self.is_fired:
                game_world.remove_object(self)

    def draw(self):
        # 발사되기 전에는 그리지 않음
        if not self.is_fired:
            return

        # 방향에 따라 화살 그리기
        if self.face_dir == 0:  # 오른쪽
            self.image.composite_draw(0, '', self.x, self.y - 5, 31, 5)
        elif self.face_dir == 1:  # 아래
            self.image.composite_draw(math.radians(270), '', self.x, self.y, 31, 5)
        elif self.face_dir == 2:  # 왼쪽
            self.image.composite_draw(math.radians(180), '', self.x, self.y - 5, 31, 5)
        elif self.face_dir == 3:  # 위
            self.image.composite_draw(math.radians(90), '', self.x, self.y, 31, 5)

        # 충돌 박스 그리기
        if self.is_fired:
            bb = self.get_bb()
            if bb:
                draw_rectangle(*bb)

    def get_bb(self):
        # 발사되기 전에는 충돌 박스 없음
        if not self.is_fired:
            return None

        # 방향에 따른 충돌 박스
        if self.face_dir == 0:  # 오른쪽
            return self.x - 16, self.y - 9, self.x + 16, self.y - 1
        elif self.face_dir == 1:  # 아래
            return self.x - 4, self.y - 16, self.x + 4, self.y + 16
        elif self.face_dir == 2:  # 왼쪽
            return self.x - 16, self.y - 9, self.x + 16, self.y - 1
        elif self.face_dir == 3:  # 위
            return self.x - 4, self.y - 16, self.x + 4, self.y + 16

    def do(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'player:goblin_arrow':
            if self.is_fired and not self.is_removed:
                self.is_removed = True
                game_world.remove_object(self)