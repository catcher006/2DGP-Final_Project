import time
import game_world
import game_framework
import random
import common
import sounds
import stage2_0_mode, stage2_1_mode, stage2_2_mode, stage2_3_mode
import stage2_4_mode, stage2_5_mode, stage2_6_mode, stage2_7_mode
import stage2_8_mode, stage2_9_mode, stage2_10_mode, stage2_11_mode
from stage2_0 import Stage2_0
from stage2_1 import Stage2_1
from stage2_2 import Stage2_2
from stage2_3 import Stage2_3
from stage2_4 import Stage2_4
from stage2_5 import Stage2_5
from stage2_6 import Stage2_6
from stage2_7 import Stage2_7
from stage2_8 import Stage2_8
from stage2_9 import Stage2_9
from stage2_10 import Stage2_10
from stage2_11 import Stage2_11
from zombie_mace import Zombie_Mace
from state_machine import StateMachine
from pico2d import load_image, load_font, get_time, draw_rectangle

# mob Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_IDLE_PER_ACTION = 2

time_out = lambda e: e[0] == 'TIMEOUT'
event_stop = lambda e: e[0] == 'STOP'

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

class Idle:
    def __init__(self, mob):
        self.mob = mob
        self.lap_count = 0
        self.prev_frame = 0

    def enter(self, e):
        # 정지 애니메이션 처음부터, 이동 정지
        self.mob.frame = random.randint(0, 1)
        self.mob.dx = 0.0
        self.mob.dy = 0.0
        self.lap_count = 0
        self.prev_frame = int(self.mob.frame)

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time
        # 정지 중에도 가벼운 프레임 애니메이션 업데이트
        delta = FRAMES_IDLE_PER_ACTION * ACTION_PER_TIME * dt
        new_frame_float = self.mob.frame + delta
        new_frame = int(new_frame_float) % 2

        # 프레임 래핑(한 바퀴) 감지
        if self.prev_frame > new_frame:
            self.lap_count += 1
        self.prev_frame = new_frame

        self.mob.frame = new_frame_float % 2

        # 2바퀴 완료 시 MOVE로 전환
        if self.lap_count >= 2:
            self.lap_count = 0
            self.mob.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # 현재 방향 기준으로 idle 이미지 그리기
        self.mob.idle_image.clip_draw(int(self.mob.frame) * 64, 64 * self.mob.face_dir, 64, 64, self.mob.x, self.mob.y, 100, 100)

class Dead:
    def __init__(self, mob):
        self.mob = mob
        self.max_frame = 5
        self.played = False
        self.spawned = False # 코인 생성 여부 플래그

    def enter(self, e):
        # 애니메이션을 처음부터 시작하고 이동 정지
        self.mob.frame = 0.0
        self.played = False
        self.mob.dx = 0.0
        self.mob.dy = 0.0
        self.spawned = False

    def exit(self, e):
        pass

    def do(self):
        # 이미 끝났으면 더 이상 진행하지 않음
        if self.played:
            # 애니메이션이 끝났고 아직 코인 생성/삭제가 되지 않았으면 처리
            if not self.spawned:
                from coin import Coin
                # 몹이 죽을 때 코인 생성
                coin = Coin()
                coin.x = self.mob.x
                coin.y = self.mob.y

                if Stage2_0.current_mode:
                    stage2_0_mode.coins.append(coin)
                elif Stage2_1.current_mode:
                    stage2_1_mode.coins.append(coin)
                elif Stage2_2.current_mode:
                    stage2_2_mode.coins.append(coin)
                elif Stage2_3.current_mode:
                    stage2_3_mode.coins.append(coin)
                elif Stage2_4.current_mode:
                    stage2_4_mode.coins.append(coin)
                elif Stage2_5.current_mode:
                    stage2_5_mode.coins.append(coin)
                elif Stage2_6.current_mode:
                    stage2_6_mode.coins.append(coin)
                elif Stage2_7.current_mode:
                    stage2_7_mode.coins.append(coin)
                elif Stage2_8.current_mode:
                    stage2_8_mode.coins.append(coin)
                elif Stage2_9.current_mode:
                    stage2_9_mode.coins.append(coin)
                elif Stage2_10.current_mode:
                    stage2_10_mode.coins.append(coin)
                elif Stage2_11.current_mode:
                    stage2_11_mode.coins.append(coin)

                game_world.add_object(coin, 2)
                game_world.add_collision_pair('player:coin', None, coin)
                # print(f"Coin created at ({coin.x}, {coin.y})")

                game_world.remove_collision_object(self.mob)
                game_world.remove_object(self.mob)

                self.spawned = True
            return

        dt = game_framework.frame_time
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        new_frame = self.mob.frame + delta

        if new_frame >= self.max_frame:
            self.mob.frame = float(self.max_frame)
            self.played = True
        else:
            self.mob.frame = new_frame

    def draw(self):
        self.mob.dead_image.clip_draw(int(self.mob.frame) * 64, 0, 64, 64, self.mob.x, self.mob.y, 100, 100)

class Attack:
    def __init__(self, mob):
        self.mob = mob
        self.lap_count = 0
        self.prev_frame = 0
        self.max_frame = 6  # attack 애니메이션 프레임 수
        self.zombie_mace = None

    def enter(self, e):
        self.mob.frame = 0.0
        self.mob.dx = 0.0
        self.mob.dy = 0.0
        self.lap_count = 0
        self.prev_frame = 0

        self.mob.is_attacking = True

        # 좀비 참조를 전달하여 Zombie_Mace 생성
        self.zombie_mace = Zombie_Mace(self.mob)
        game_world.add_object(self.zombie_mace, 2)

        # 충돌 그룹에 추가
        if Stage2_0.current_mode or Stage2_1.current_mode or Stage2_2.current_mode or Stage2_3.current_mode or Stage2_4.current_mode or \
                Stage2_5.current_mode or Stage2_6.current_mode or Stage2_7.current_mode or Stage2_8.current_mode or Stage2_9.current_mode or \
                Stage2_10.current_mode or Stage2_11.current_mode:
            game_world.add_collision_pair('player:zombie_mace', None, self.zombie_mace)
            # 플레이어와 충돌 페어 추가
            for layer in game_world.world:
                for obj in layer:
                    if hasattr(obj, 'handle_collision') and 'player' in str(type(obj)).lower():
                        game_world.add_collision_pair('player:zombie_mace', obj, None)

    def exit(self, e):
        self.mob.is_attacking = False
        self.mob.frame = 0

        self.zombie_mace = None

    def do(self):
        dt = game_framework.frame_time
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        new_frame_float = self.mob.frame + delta
        new_frame = int(new_frame_float) % self.max_frame

        # 프레임 래핑(한 바퀴) 감지
        if self.prev_frame > new_frame:
            self.lap_count += 1
        self.prev_frame = new_frame

        self.mob.frame = new_frame_float % self.max_frame

        # 1바퀴 완료 시 MOVE로 전환
        if self.lap_count >= 1:
            self.lap_count = 0
            self.mob.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        self.mob.attack_image.clip_draw(int(self.mob.frame) * 192, 192 * self.mob.face_dir, 192, 192, self.mob.x, self.mob.y, 300, 300)

class Move:
    def __init__(self, mob):
        self.mob = mob

    def enter(self, e):
        self.mob.frame = random.randint(0, 5)
        self.timer = 0.0  # 별도 타이머 추가
        self.lap_count = 0
        self.prev_frame = int(self.mob.frame)

        self.mob.lr_dir = random.randint(-1, 1)
        if self.mob.lr_dir == 0:
            self.mob.ud_dir = random.choice([-1, 1])
        else:
            self.mob.ud_dir = 0

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time

        # 프레임 애니메이션 (0~5), 랩(한바퀴) 감지
        delta = FRAMES_PER_ACTION * ACTION_PER_TIME * dt
        new_frame_float = self.mob.frame + delta
        new_frame = int(new_frame_float) % 6

        # 프레임이 래핑되면 한 바퀴 완료로 간주
        if self.prev_frame > new_frame:
            self.lap_count += 1
        self.prev_frame = new_frame

        self.mob.frame = new_frame_float % 6

        # 4바퀴마다 방향 변경 후 정지 상태로 전환(확률 제거, 항상 STOP)
        if self.lap_count >= 4:
            self.mob.lr_dir = random.randint(-1, 1)
            if self.mob.lr_dir == 0:
                self.mob.ud_dir = random.choice([-1, 1])
            else:
                self.mob.ud_dir = 0

            self.lap_count = 0
            self.timer = 0.0
            self.mob.state_machine.handle_state_event(('STOP', None))
            return

        # 이동 벡터 계산
        dx = self.mob.lr_dir * RUN_SPEED_PPS * dt
        dy = self.mob.ud_dir * RUN_SPEED_PPS * dt

        self.mob.dx = dx
        self.mob.dy = dy

        new_x = self.mob.x + self.mob.dx
        new_y = self.mob.y + self.mob.dy

        can_move = self.mob.can_move_to(new_x, new_y)

        if can_move:
            self.mob.x = new_x
            self.mob.y = new_y

    def draw(self):
        if self.mob.ud_dir == 1: self.mob.face_dir = 3
        elif self.mob.lr_dir == -1: self.mob.face_dir = 2
        elif self.mob.ud_dir == -1: self.mob.face_dir = 1
        elif self.mob.lr_dir == 1: self.mob.face_dir = 0

        self.mob.move_image.clip_draw(int(self.mob.frame) * 64, 64 * self.mob.face_dir, 64, 64, self.mob.x, self.mob.y, 100, 100)

class Zombie_Mob:
    def __init__(self):
        self.mob_type = random.choice(["none", "mace"])

        self.move_image = load_image("./image/mobs/zombie/" + self.mob_type + "/walk.png")
        self.idle_image = load_image("./image/mobs/zombie/" + self.mob_type + "/idle.png")
        self.dead_image = load_image("./image/mobs/zombie/" + self.mob_type + "/dead.png")
        if self.mob_type == "mace":
            self.attack_image = load_image("./image/mobs/zombie/" + self.mob_type + "/attack.png")

        self.hp_image = load_image("./image/ui/mobs/zombie/zombie_hp.png")

        self.font = load_font('./font/ENCR10B.TTF', 10)

        self.x = random.randint(105,940)
        self.y = random.randint(85,540)

        self.frame = random.randint(0,5)
        self.is_move = True

        self.dx = 0.0
        self.dy = 0.0

        self.ud_dir = 0  # up down direction (up: 1, down: -1, none: 0)
        self.lr_dir = 0  # left right direction (left: -1, right: 1, none: 0)

        self.face_dir = 0  # 마지막 방향 저장 (0: 오른쪽, 1: 아래, 2: 왼쪽, 3: 위)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.hp = 100  # 체력
        self.is_alive = True  # 생존 상태
        self.is_attacking = False

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

        # 상태 머신 생성
        if self.mob_type == "mace":
            self.ATTACK = Attack(self)
            # mace 타입
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE: {time_out: self.MOVE, event_die: self.DEAD},
                    self.MOVE: {event_die: self.DEAD, event_stop: self.ATTACK},
                    self.ATTACK: {time_out: self.MOVE, event_die: self.DEAD},
                    self.DEAD: {}
                }
            )
        else:
            # none 타입
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.MOVE: {event_die: self.DEAD, event_stop: self.IDLE},
                    self.IDLE: {time_out: self.MOVE, event_die: self.DEAD},
                    self.DEAD: {}
                }
            )

    def draw(self):
        self.state_machine.draw()

        if self.is_alive or self.hp > 0:
            self.hp_image.clip_draw(0, int(self.hp) * 54, 400, 54, self.x, self.y + 35, 60, 11)
            if self.hp >= 100:
                self.font.draw(self.x - 9, self.y + 35, f'{self.hp:02d}', (255, 255, 255))
            elif 50 < self.hp < 100:
                self.font.draw(self.x - 9, self.y + 35, f'{self.hp:02d}', (255, 255, 255))
            elif self.hp == 50:
                self.font.draw(self.x - 9, self.y + 35, '5', (255, 255, 255))
                self.font.draw(self.x - 4, self.y + 35, '0', (168, 190, 208))
            else:
                self.font.draw(self.x - 9, self.y + 35, f'{self.hp:02d}', (168, 190, 208))
            # draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not self.is_alive or self.hp <= 0:
            return None

        if self.face_dir == 3:
            return self.x - 22, self.y - 47, self.x + 22, self.y + 25
        elif self.face_dir == 2:
            return self.x - 15, self.y - 47, self.x + 15, self.y + 25
        elif self.face_dir == 1:
            return self.x - 22, self.y - 47, self.x + 22, self.y + 25
        elif self.face_dir == 0:
            return self.x - 18, self.y - 47, self.x + 15, self.y + 25

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

        if group == 'player_sword:zombie_mob' and self.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                # 데미지 처리
                self.apply_damage()
                self.last_damage_time = current_time

                # 칼 넉백 (플레이어 반대 방향)
                self.apply_knockback(other, 15, 1.5)

        elif group == 'player_arrow:zombie_mob' and self.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                # 데미지 처리
                self.apply_damage()
                self.last_damage_time = current_time

                # 화살 넉백 (화살 방향으로, 더 강함)
                self.apply_knockback(other, 20, 2.0)

        elif group == 'player:zombie_mob' and self.is_alive:
            self.apply_knockback(other, 20, 1.0)

        elif group == 'zombie_mob:zombie_mob' and self.is_alive:
            self.apply_knockback(other, 5, 0.5)

    def apply_damage(self):
        if common.player.current_weapon_id in ['normal_sword', 'normal_bow']:
            self.hp -= 20
        elif common.player.current_weapon_id in ['silver_sword', 'silver_bow']:
            self.hp -= 50
        elif common.player.current_weapon_id in ['gold_sword', 'gold_bow']:
            self.hp -= 100

        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            sounds.zombie_dead_sound.play()
            self.state_machine.handle_state_event(('DIE', None))
            # print("zombie_mob is dead!")
        else:
            sounds.zombie_hurt_sound.play()
            # print(f"zombie_mob damaged! HP: {self.hp}")

    def apply_knockback(self, other, distance, multiplier):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist > 0:
            nx = dx / dist
            ny = dy / dist

            self.is_knocked_back = True
            self.knockback_distance = distance
            self.knockback_dx = nx * multiplier
            self.knockback_dy = ny * multiplier