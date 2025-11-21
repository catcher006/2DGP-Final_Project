import time
import game_framework
import game_world
from player_sword import Player_Sword
from stage1_0 import Stage1_0
from stage1_1 import Stage1_1
from stage1_2 import Stage1_2
from stage1_3 import Stage1_3
from stage1_4 import Stage1_4
from stage1_5 import Stage1_5
from stage1_6 import Stage1_6
from stage1_7 import Stage1_7
from state_machine import StateMachine
from pico2d import *
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_f, SDLK_SPACE

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# By Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_IDLE_ACTION = 2
FRAMES_PER_DEAD_ACTION = 6

# 모드 호환을 위한 전역 변수 사용
player_x = 0
player_y = 0
player_frame = 0
player_face_dir = 0
player_hp = 100
player_is_alive = True
player_is_attacking = False
player_plate_id = 'normalplate'
player_weapon_id = 'goldsword'

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

def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def event_die(e):
    return e[0] == 'DIE'

def space_down(e):  # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def check_weapon():
    if player_weapon_id in ['normalsword', 'silversword', 'goldsword']:
        return 'sword'
    elif player_weapon_id in ['normalbow', 'silverbow', 'goldbow']:
        return 'bow'
    else:
        return 'none'


class Dead:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0
        print("Entered Dead state!")  # 디버그용

    def exit(self, e):
        pass

    def do(self):
        if self.player.frame < 5:
            self.player.frame += FRAMES_PER_DEAD_ACTION * ACTION_PER_TIME * game_framework.frame_time


    def draw(self):
        self.player.dead_image.clip_draw(int(self.player.frame) * 64, 0, 64, 64, self.player.x, self.player.y, 100, 100)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass
    def exit(self, e):
        pass

    def do(self):
        if self.player.ydir == 1:
            self.player.face_dir = 3
        elif self.player.xdir == -1:
            self.player.face_dir = 2
        elif self.player.ydir == -1:
            self.player.face_dir = 1
        elif self.player.xdir == 1:
            self.player.face_dir = 0

        global player_x, player_y
        player_x = self.player.x
        player_y = self.player.y

        self.player.frame = (self.player.frame + FRAMES_PER_IDLE_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2


    def draw(self):
        from stage1_0 import Stage1_0

        if not Stage1_0.stage1_0_create or player_weapon_id == 'none':
            self.player.idle_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64, self.player.x, self.player.y, 100, 100)
        else:
            self.player.combat_idle_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64, self.player.x, self.player.y, 100, 100)

class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.frame_time
        # 이동 벡터를 먼저 계산 (px per second * dt)
        dx = self.player.xdir * RUN_SPEED_PPS * dt
        dy = self.player.ydir * RUN_SPEED_PPS * dt

        # 디버깅용으로 player에 저장해두면 유용
        self.player.dx = dx
        self.player.dy = dy

        new_x = self.player.x + self.player.dx
        new_y = self.player.y + self.player.dy

        # print(f"Trying to move to ({new_x}, {new_y})")

        # 실제 이동 가능 여부 검사
        can_move = self.player.can_move_to(new_x, new_y)

        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9

        if can_move:
            self.player.x = new_x
            self.player.y = new_y

        global player_x, player_y
        player_x = self.player.x
        player_y = self.player.y

    def draw(self):
        if self.player.ydir == 1: self.player.face_dir = 3
        elif self.player.xdir == -1: self.player.face_dir = 2
        elif self.player.ydir == -1: self.player.face_dir = 1
        elif self.player.xdir == 1: self.player.face_dir = 0

        global player_face_dir
        player_face_dir = self.player.face_dir

        if check_weapon() is 'bow':
            self.player.walk_image.clip_draw(int(self.player.frame) * 128, 128 * self.player.face_dir, 128, 128, self.player.x, self.player.y, 200, 200)
        else:
            self.player.walk_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64,self.player.x, self.player.y, 100, 100)


class Attack:
    def __init__(self, player):
        self.player = player
        self.player_sword = None # 검 객체 참조 저장

    def enter(self, e):
        self.player.is_attacking = True
        global player_is_attacking
        player_is_attacking = True
        self.player.attack_start_time = time.time()
        self.player.frame = 0

        # 공격 시작할 때 Player_Sword 객체를 생성하고 게임 월드에 추가
        self.player_sword = Player_Sword()
        game_world.add_object(self.player_sword, 2)

        # 충돌 그룹에 추가
        if Stage1_0.current_mode or Stage1_1.current_mode or Stage1_2.current_mode or Stage1_3.current_mode or Stage1_5.current_mode or Stage1_6.current_mode or Stage1_7.current_mode:
            game_world.add_collision_pair('player_sword:slime_mob', self.player_sword, None)
            # 기존 슬라임들과 충돌 페어 추가
            for layer in game_world.world:
                for obj in layer:
                    if hasattr(obj, 'handle_collision') and 'slime' in str(type(obj)).lower():
                        game_world.add_collision_pair('player_sword:slime_mob', None, obj)

        elif Stage1_4.current_mode:
            game_world.add_collision_pair('player_sword:slime_boss', self.player_sword, None)
            # 기존 슬라임 보스와 충돌 페어 추가
            for layer in game_world.world:
                for obj in layer:
                    if hasattr(obj, 'handle_collision') and 'slime_boss' in str(type(obj)).lower():
                        game_world.add_collision_pair('player_sword:slime_boss', None, obj)

    def exit(self, e):
        self.player.is_attacking = False
        self.player.frame = 0

        global player_frame, player_is_attacking
        player_frame = 0
        player_is_attacking = False

        self.player_sword = None

    def do(self):
        if check_weapon() is 'none':
            # 무기가 없으면 공격 상태에서 바로 대기 상태로 전환
            self.player.state_machine.handle_state_event(('STOP', None))
            return
        # 공격 애니메이션 처리
        if self.player.frame < 13:
            self.player.frame += FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            global player_frame
            player_frame = self.player.frame
        else:
            # 공격 애니메이션이 끝나면 대기 상태로 전환
            self.player.state_machine.handle_state_event(('STOP', None))

    def draw(self):
        if check_weapon() is 'sword':
            self.player.sword_image.clip_draw(int(self.player.frame) * 128, 128 * self.player.face_dir, 128, 128, self.player.x, self.player.y, 200, 200)
        elif check_weapon() is 'bow':
            self.player.bow_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64,self.player.x, self.player.y, 100, 100)

class Player:
    walk_image = None
    idle_image = None
    dead_image = None
    sword_image = None
    combat_idle_image = None
    bow_image = None

    def load_walk_images(self):
        if Player.walk_image is None:
            Player.walk_image = load_image('./image/player/' + player_plate_id + '/' + player_weapon_id + '/' + 'walk.png')

    def load_idle_images(self):
        if Player.idle_image is None:
            Player.idle_image = load_image('./image/player/' + player_plate_id + '/' + player_weapon_id + '/' + 'idle.png')

    def load_dead_images(self):
        if Player.dead_image is None:
            Player.dead_image = load_image('./image/player/' + player_plate_id + '/' + player_weapon_id + '/' + 'dead.png')

    def load_sword_images(self):
        if Player.sword_image is None:
            if check_weapon() is 'sword':
                Player.sword_image = load_image('./image/player/' + player_plate_id + '/' + player_weapon_id + '/' + 'sword_attack.png')

    def load_bow_images(self):
        if Player.sword_image is None:
            if check_weapon() is 'bow':
                Player.bow_image = load_image('./image/player/' + player_plate_id + '/' + player_weapon_id + '/' + 'bow_attack.png')

    def load_combat_idle_images(self):
        if Player.combat_idle_image is None:
            Player.combat_idle_image = load_image('./image/player/' + player_plate_id + '/' + player_weapon_id + '/' + 'combat_idle.png')

    def __init__(self):
        self.load_walk_images()
        self.load_idle_images()
        self.load_dead_images()
        if check_weapon() is 'sword':
            self.load_sword_images()
        elif check_weapon() is 'bow':
            self.load_bow_images()
        self.load_combat_idle_images()

        self.font = load_font('ENCR10B.TTF', 16)

        self.x = 510
        self.y = 160

        global player_x, player_y
        player_x = self.x
        player_y = self.y

        self.frame = 0

        self.dx = 0.0
        self.dy = 0.0

        self.xdir = 0 # up down direction (up: 1, down: -1, none: 0)
        self.ydir = 0 # left right direction (left: -1, right: 1, none: 0)

        self.face_dir = 0 # 마지막 방향 저장 (0: 오른쪽, 1: 아래, 2: 왼쪽, 3: 위)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        self.is_attacking = False  # 공격 상태
        self.attack_start_time = 0  # 공격 시작 시간

        # 데미지 관련
        self.last_damage_time = 0
        self.damage_cooldown = TIME_PER_ACTION * 1

        # 넉백 관련
        self.is_knocked_back = False
        self.knockback_distance = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

        # 상태들 생성
        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.DEAD = Dead(self)
        self.ATTACK = Attack(self)

        # 상태 머신 생성
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: { event_run: self.WALK, space_down: self.ATTACK, event_die: self.DEAD },
                self.WALK: { event_stop: self.IDLE, space_down: self.ATTACK, event_die: self.DEAD },
                self.ATTACK: { event_stop: self.IDLE, event_die: self.DEAD },
                self.DEAD: {}
            }

        )

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 35, self.y + 40, f'hp: {player_hp:02d}', (255, 0, 255))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
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

                    global player_x, player_y
                    player_x = self.x
                    player_y = self.y

                self.knockback_distance -= 1
            else:
                self.is_knocked_back = False
                self.knockback_dx = 0
                self.knockback_dy = 0

        self.state_machine.update()

    def handle_event(self, event):
        # 죽었으면 입력 무시
        if not player_is_alive:
            return

        if event.key in (SDLK_a, SDLK_d, SDLK_w, SDLK_s):
            cur_xdir, cur_ydir = self.xdir, self.ydir
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_a: self.xdir -= 1
                elif event.key == SDLK_d: self.xdir += 1
                elif event.key == SDLK_w: self.ydir += 1
                elif event.key == SDLK_s: self.ydir -= 1
            elif event.type == SDL_KEYUP:
                # 키를 떼는 순간에도 방향 값을 0으로 직접 설정
                if event.key == SDLK_a and self.xdir < 0: self.xdir = 0
                elif event.key == SDLK_d and self.xdir > 0: self.xdir = 0
                elif event.key == SDLK_w and self.ydir > 0: self.ydir = 0
                elif event.key == SDLK_s and self.ydir < 0: self.ydir = 0
            if cur_xdir != self.xdir or cur_ydir != self.ydir:  # 방향키에 따른 변화가 있으면
                if self.xdir == 0 and self.ydir == 0:  # 멈춤
                    self.state_machine.handle_state_event(('STOP', self.face_dir))  # 스탑 시 이전 방향 전달
                else:  # 움직임
                    self.state_machine.handle_state_event(('RUN', None))
        else:
            # 공격키일 때 현재 공격 가능 여부 확인
            if space_down(('INPUT', event)) and not Stage1_0.stage1_0_create:
                return
            self.state_machine.handle_state_event(('INPUT', event))

    def can_move_to(self, x, y):
        if callable(self.move_validator):
            return self.move_validator(x, y)

        return False

    def handle_collision(self, group, other):
        global player_hp, player_is_alive

        if group == 'player:slime_mob' and player_is_alive:
            current_time = time.time()

            # 마지막 데미지로부터 충분한 시간이 지났는지 확인
            if current_time - self.last_damage_time >= self.damage_cooldown:
                player_hp -= 10
                self.last_damage_time = current_time

                # 넉백 방향 계산 (플레이어 -> 슬라임의 반대 방향)
                dx = self.x - other.x
                dy = self.y - other.y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance > 0:
                    # 정규화된 방향 벡터
                    nx = dx / distance
                    ny = dy / distance

                    # 넉백 설정 (20픽셀을 20프레임에 걸쳐 이동)
                    self.is_knocked_back = True
                    self.knockback_distance = 20
                    self.knockback_dx = nx * 1.0
                    self.knockback_dy = ny * 1.0

                if player_hp <= 0:
                    player_is_alive = False
                    self.state_machine.handle_state_event(('DIE', None))
                    print("Player is dead!")

                # 디버그 출력 (선택사항)
                print(f"Player damaged! HP: {player_hp}")

        elif group == 'player:coin':
            pass

        elif group == 'player:slime_boss' and player_is_alive:
            current_time = time.time()

            # 마지막 데미지로부터 충분한 시간이 지났는지 확인
            if current_time - self.last_damage_time >= self.damage_cooldown:
                player_hp -= 20
                self.last_damage_time = current_time

                # 보스와 충돌 시 넉백 (더 강한 넉백)
                dx = self.x - other.x
                dy = self.y - other.y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance > 0:
                    nx = dx / distance
                    ny = dy / distance

                    # 보스는 넉백이 더 강함
                    self.is_knocked_back = True
                    self.knockback_distance = 30
                    self.knockback_dx = nx * 3.0
                    self.knockback_dy = ny * 3.0

                if player_hp <= 0:
                    player_hp = 0
                    player_is_alive = False
                    self.state_machine.handle_state_event(('DIE', None))
                    print("Player is dead!")

                # 디버그 출력 (선택사항)
                print(f"Player damaged! HP: {player_hp}")
