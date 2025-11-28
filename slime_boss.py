import time
import game_world
import game_framework
import random
import stage1_0_mode, stage1_1_mode, stage1_2_mode, stage1_3_mode
import stage1_4_mode, stage1_5_mode, stage1_6_mode, stage1_7_mode
from stage1_0 import Stage1_0
from stage1_1 import Stage1_1
from stage1_2 import Stage1_2
from stage1_3 import Stage1_3
from stage1_4 import Stage1_4
from stage1_5 import Stage1_5
from stage1_6 import Stage1_6
from stage1_7 import Stage1_7
from player import player_weapon_id
from state_machine import StateMachine
from coin import Coin
from pico2d import load_image, load_font, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f


# mob Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# By Action Speed
TIME_PER_ACTION = 0.75
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

time_out = lambda e: e[0] == 'TIMEOUT'

def event_die(e):
    return e[0] == 'DIE'

# 점 (x, y)가 다각형 내부에 있는지 확인하는 함수
def point_in_polygon(x, y, polygon):
    n = len(polygon)
    inside = False

    j = n - 1
    for i in range(n):
        if ((polygon[i][1] > y) != (polygon[j][1] > y)) and \
           (x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            inside = not inside
        j = i

    return inside

class Dead:
    def __init__(self, boss_mob):
        self.boss_mob = boss_mob
        self.max_frame = 5
        self.played = False
        self.spawned = False # 코인 생성 여부 플래그

    def enter(self, e):
        # 애니메이션을 처음부터 시작하고 이동 정지
        self.boss_mob.frame = 0.0
        self.played = False
        self.boss_mob.dx = 0.0
        self.boss_mob.dy = 0.0
        self.spawned = False

    def exit(self, e):
        pass

    def do(self):
        # 이미 끝났으면 더 이상 진행하지 않음
        if self.played:
            # 애니메이션이 끝났고 아직 코인 생성/삭제가 되지 않았으면 처리
            if not self.spawned:
                # 보스가 죽을 때 8개의 코인 생성
                coin_positions = [
                    (self.boss_mob.x, self.boss_mob.y + 30), (self.boss_mob.x - 30, self.boss_mob.y),
                    (self.boss_mob.x + 30, self.boss_mob.y), (self.boss_mob.x, self.boss_mob.y - 30)
                ]

                for pos in coin_positions:
                    coin = Coin()
                    coin.x, coin.y = pos
                    coin.frame = random.randint(0, 7)

                    if Stage1_4.current_mode:
                        stage1_4_mode.coins.append(coin)

                    game_world.add_object(coin, 2)
                    game_world.add_collision_pair('player:coin', None, coin)

                print(f"8 coins created around boss at ({self.boss_mob.x}, {self.boss_mob.y})")

                game_world.remove_object(self.boss_mob)

                self.spawned = True
            return

        dt = game_framework.frame_time
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        new_frame = self.boss_mob.frame + delta

        if new_frame >= self.max_frame:
            self.boss_mob.frame = float(self.max_frame)
            self.played = True
        else:
            self.boss_mob.frame = new_frame

    def draw(self):
        self.boss_mob.dead_image.clip_draw(int(self.boss_mob.frame) * 30, 0, 30, 26, self.boss_mob.x, self.boss_mob.y, 192, 124)

class Idle:
    def __init__(self, boss_mob):
        self.boss_mob = boss_mob

    def enter(self, e):
        # 방향을 랜덤으로 설정
        self.boss_mob.lr_dir = random.randint(-1, 1)
        if self.boss_mob.lr_dir == 0:
            self.boss_mob.ud_dir = random.choice([-1, 1])
        else:
            self.boss_mob.ud_dir = 0
        self.boss_mob.frame = random.randint(0, 5)
        self.timer = 0.0  # 별도 타이머 추가

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time

        # 타이머 증가
        self.timer += dt

        # 4바퀴 시간 (24프레임 * 0.5초 / 8프레임 = 1.5초)
        if self.timer >= 1.5:
            self.boss_mob.state_machine.handle_state_event(('TIMEOUT', 0))
            return

        # 프레임 애니메이션 (0~5 범위 유지)
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        self.boss_mob.frame = (self.boss_mob.frame + delta) % 6

    def draw(self):
        self.boss_mob.idle_image.clip_draw(int(self.boss_mob.frame) * 48, 0, 48, 31, self.boss_mob.x, self.boss_mob.y, 192, 124)

class Move:
    def __init__(self, boss_mob):
        self.boss_mob = boss_mob

    def enter(self, e):
        self.boss_mob.frame = random.randint(0, 5)
        self.timer = 0.0  # 별도 타이머 추가

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time

        # 타이머 증가
        self.timer += dt

        # 2바퀴 시간 (12프레임 * 0.5초 / 8프레임 = 0.75초)
        if self.timer >= 0.75:
            self.boss_mob.state_machine.handle_state_event(('TIMEOUT', 0))
            return

        # 프레임 애니메이션 (0~5 범위 유지)
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        self.boss_mob.frame = (self.boss_mob.frame + delta) % 6

        # 이동 벡터 계산
        dx = self.boss_mob.lr_dir * RUN_SPEED_PPS * dt
        dy = self.boss_mob.ud_dir * RUN_SPEED_PPS * dt

        self.boss_mob.dx = dx
        self.boss_mob.dy = dy

        new_x = self.boss_mob.x + self.boss_mob.dx
        new_y = self.boss_mob.y + self.boss_mob.dy

        can_move = self.boss_mob.can_move_to(new_x, new_y)

        if can_move:
            self.boss_mob.x = new_x
            self.boss_mob.y = new_y

    def draw(self):
        self.boss_mob.move_image.clip_draw(int(self.boss_mob.frame) * 48, 0, 48, 31, self.boss_mob.x, self.boss_mob.y, 192, 124)

class Slime_Boss:
    def __init__(self):
        self.move_image = load_image("./image/mobs/slime_boss/slime_boss_jump.png")
        self.idle_image = load_image("./image/mobs/slime_boss/slime_boss_jump.png")
        self.dead_image = load_image("./image/mobs/slime_boss/slime_boss_dead.png")

        self.hp_image = load_image("./image/ui/mobs/slime_boss/boss_slime_hp.png")

        self.font = load_font('ENCR10B.TTF', 10)

        self.x = random.randint(155,890)
        self.y = random.randint(135,490)

        self.frame = random.randint(0,5)
        self.is_move = True

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0  # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0  # left right direction (left: -1, right: 1, none: 0)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.hp = 200  # 체력
        self.is_alive = True  # 생존 상태

        # 데미지 관련
        self.last_damage_time = 0
        self.damage_cooldown = TIME_PER_ACTION

        # 넉백 관련
        self.is_knocked_back = False
        self.knockback_distance = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.DEAD = Dead(self)

        # is_move 값에 따라 초기 상태 결정
        initial_state = self.MOVE if self.is_move else self.IDLE

        # 상태 머신 생성
        self.state_machine = StateMachine(
            initial_state,
            {
                self.MOVE: {time_out: self.IDLE, event_die: Dead(self)},
                self.IDLE: {time_out: self.MOVE, event_die: Dead(self)},
                self.DEAD: {}
            }
        )

    def draw(self):
        self.state_machine.draw()

        if self.is_alive or self.hp > 0:
            self.hp_image.clip_draw(0, self.hp // 5 * 66, 240, 66, self.x - 15, self.y + 65, 60, 11)
            if self.hp > 100:
                self.font.draw(self.x - 23, self.y + 65, f'{self.hp:02d}', (255, 255, 255))
            elif self.hp == 100:
                self.font.draw(self.x - 21, self.y + 65, '1', (255, 255, 255))
                self.font.draw(self.x - 15, self.y + 65, '00', (255, 0, 0))
            else:
                self.font.draw(self.x - 21, self.y + 65, f'{self.hp:02d}', (255, 0, 0))

            draw_rectangle(*self.get_bb())

    def get_bb(self):
        frame = int(self.frame)  # frame을 정수로 변환

        if not self.is_alive or self.hp <= 0:
            return None

        if frame == 0:
            return self.x - 90, self.y - 60, self.x + 60, self.y + 30
        elif frame == 1:
            return self.x - 90, self.y - 64, self.x + 60, self.y + 24
        elif frame == 2:
            return self.x - 76, self.y - 60, self.x + 50, self.y + 48
        elif frame == 3:
            return self.x - 76, self.y - 48, self.x + 50, self.y + 60
        elif frame == 4:
            return self.x - 76, self.y - 60, self.x + 50, self.y + 48
        elif frame == 5:
            return self.x - 96, self.y - 64, self.x + 70, self.y + 24

    def update(self):
        # 넉백 중이면 넉백 처리
        if self.is_knocked_back:
            if self.knockback_distance > 0:
                # 이동 가능한 위치인지 확인
                new_x = self.x + self.knockback_dx
                new_y = self.y + self.knockback_dy

                if self.can_move_to(new_x, new_y):
                    self.x = new_x
                    self.y = new_y

                self.knockback_distance -= 1
            else:
                self.is_knocked_back = False
                self.knockback_dx = 0
                self.knockback_dy = 0

        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def can_move_to(self, x, y):
        if callable(self.move_validator):
            return self.move_validator(x, y)

        return False

    def handle_collision(self, group, other):
        if not self.is_alive:
            return

        if group == 'player_sword:slime_boss' and self.is_alive:
            current_time = time.time()

            # 마지막 데미지로부터 충분한 시간이 지났는지 확인
            if current_time - self.last_damage_time >= self.damage_cooldown:
                if player_weapon_id == 'normalsword':
                    self.hp -= 20
                elif player_weapon_id == 'silversword':
                    self.hp -= 50
                elif player_weapon_id == 'goldsword':
                    self.hp -= 100
                self.last_damage_time = current_time

                # 칼에 맞았을 때 넉백 (플레이어 반대 방향)
                dx = self.x - other.x
                dy = self.y - other.y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance > 0:
                    nx = dx / distance
                    ny = dy / distance

                    self.is_knocked_back = True
                    self.knockback_distance = 15
                    self.knockback_dx = nx * 1.5
                    self.knockback_dy = ny * 1.5

                if self.hp <= 0:
                    self.hp = 0
                    self.is_alive = False
                    Stage1_4.boss_cleared = True
                    self.state_machine.handle_state_event(('DIE', None))
                    print("slime_mob is dead!")

                # 디버그 출력 (선택사항)
                print(f"slime_mob damaged! HP: {self.hp}")

        elif group == 'player_arrow:slime_boss' and self.is_alive:
            current_time = time.time()

            if current_time - self.last_damage_time >= self.damage_cooldown:
                if player_weapon_id == 'normalbow':
                    self.hp -= 20
                elif player_weapon_id == 'silverbow':
                    self.hp -= 50
                elif player_weapon_id == 'goldbow':
                    self.hp -= 100
                self.last_damage_time = current_time

                # 화살에 맞았을 때 넉백 (화살 방향으로)
                dx = self.x - other.x
                dy = self.y - other.y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance > 0:
                    nx = dx / distance
                    ny = dy / distance

                    self.is_knocked_back = True
                    self.knockback_distance = 20
                    self.knockback_dx = nx * 2.0
                    self.knockback_dy = ny * 2.0

                if self.hp <= 0:
                    self.hp = 0
                    self.is_alive = False
                    Stage1_4.boss_cleared = True
                    self.state_machine.handle_state_event(('DIE', None))
                    print("slime_mob is dead!")

                print(f"slime_mob damaged by arrow! HP: {self.hp}")

        elif group == 'player:slime_boss' and self.is_alive:
            # 넉백 방향 계산
            dx = self.x - other.x
            dy = self.y - other.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 0:
                # 정규화된 방향 벡터
                nx = dx / distance
                ny = dy / distance

                # 넉백 설정
                self.is_knocked_back = True
                self.knockback_distance = 30
                self.knockback_dx = nx * 1.5
                self.knockback_dy = ny * 1.5