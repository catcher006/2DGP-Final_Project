import time
import game_framework
import game_world
import sounds
from player_sword import Player_Sword
from player_arrow import Player_Arrow
from stage1_0 import Stage1_0
from stage1_1 import Stage1_1
from stage1_2 import Stage1_2
from stage1_3 import Stage1_3
from stage1_4 import Stage1_4
from stage1_5 import Stage1_5
from stage1_6 import Stage1_6
from stage1_7 import Stage1_7
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
from stage3_0 import Stage3_0
from stage3_1 import Stage3_1
from stage3_2 import Stage3_2
from stage3_3 import Stage3_3
from stage3_4 import Stage3_4
from stage3_5 import Stage3_5
from stage3_6 import Stage3_6
from stage3_7 import Stage3_7
from stage3_8 import Stage3_8
from stage3_9 import Stage3_9
from stage3_10 import Stage3_10
from stage3_11 import Stage3_11
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
player_hp = 100

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


class Dead:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0
        # print("Entered Dead state!")  # 디버그용

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

        self.player.frame = (self.player.frame + FRAMES_PER_IDLE_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2


    def draw(self):
        if not Stage1_0.stage1_0_create or self.player.current_weapon_id == 'none':
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

    def draw(self):
        if self.player.ydir == 1: self.player.face_dir = 3
        elif self.player.xdir == -1: self.player.face_dir = 2
        elif self.player.ydir == -1: self.player.face_dir = 1
        elif self.player.xdir == 1: self.player.face_dir = 0

        if self.player.check_weapon() == 'bow':
            self.player.walk_image.clip_draw(int(self.player.frame) * 128, 128 * self.player.face_dir, 128, 128, self.player.x, self.player.y, 200, 200)
        else:
            self.player.walk_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64,self.player.x, self.player.y, 100, 100)


class Attack:
    def __init__(self, player):
        self.player = player
        self.player_sword = None # 검 객체 참조 저장
        self.player_arrow = None # 화살 객체 참조 저장

    def enter(self, e):
        Player.is_attacking = True
        self.player.attack_start_time = time.time()
        self.player.frame = 0

        if self.player.check_weapon() == 'sword':

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

            elif Stage2_0.current_mode or Stage2_1.current_mode or Stage2_2.current_mode or Stage2_3.current_mode or Stage2_4.current_mode or \
                    Stage2_5.current_mode or Stage2_6.current_mode or Stage2_8.current_mode or Stage2_9.current_mode or \
                    Stage2_10.current_mode or Stage2_11.current_mode:
                game_world.add_collision_pair('player_sword:zombie_mob', self.player_sword, None)
                # 기존 몹들과 충돌 페어 추가
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'zombie' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_sword:zombie_mob', None, obj)

            elif Stage2_7.current_mode:
                game_world.add_collision_pair('player_sword:zombie_boss', self.player_sword, None)
                # 기존 좀비 보스와 충돌 페어 추가
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'zombie_boss' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_sword:zombie_boss', None, obj)

            elif Stage3_0.current_mode or Stage3_1.current_mode or Stage3_2.current_mode or Stage3_3.current_mode or Stage3_4.current_mode or \
                    Stage3_5.current_mode or Stage3_6.current_mode or Stage3_8.current_mode or \
                    Stage3_9.current_mode or Stage3_10.current_mode or Stage3_11.current_mode:
                game_world.add_collision_pair('player_sword:goblin_mob', self.player_sword, None)
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'goblin_mob' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_sword:goblin_mob', None, obj)

            if Stage3_7.current_mode:
                game_world.add_collision_pair('player_sword:goblin_boss', self.player_sword, None)
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'goblin_boss' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_sword:goblin_boss', None, obj)

        elif self.player.check_weapon() == 'bow':
            self.player_arrow = Player_Arrow()
            game_world.add_object(self.player_arrow, 2)

            # 충돌 페어 추가
            if Stage1_0.current_mode or Stage1_1.current_mode or Stage1_2.current_mode or Stage1_3.current_mode or Stage1_5.current_mode or Stage1_6.current_mode or Stage1_7.current_mode:
                game_world.add_collision_pair('player_arrow:slime_mob', self.player_arrow, None)
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'slime' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_arrow:slime_mob', None, obj)

            elif Stage1_4.current_mode:
                game_world.add_collision_pair('player_arrow:slime_boss', self.player_arrow, None)
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'slime_boss' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_arrow:slime_boss', None, obj)

            elif Stage2_0.current_mode or Stage2_1.current_mode or Stage2_2.current_mode or Stage2_3.current_mode or Stage2_4.current_mode or \
                    Stage2_5.current_mode or Stage2_6.current_mode or Stage2_8.current_mode or Stage2_9.current_mode or \
                    Stage2_10.current_mode or Stage2_11.current_mode:
                game_world.add_collision_pair('player_arrow:zombie_mob', self.player_arrow, None)
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'zombie' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_arrow:zombie_mob', None, obj)

            elif Stage2_7.current_mode:
                game_world.add_collision_pair('player_arrow:zombie_boss', self.player_arrow, None)
                # 기존 좀비 보스와 충돌 페어 추가
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'zombie_boss' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_arrow:zombie_boss', None, obj)

            elif Stage3_0.current_mode or Stage3_1.current_mode or Stage3_2.current_mode or Stage3_3.current_mode or Stage3_4.current_mode or \
                    Stage3_5.current_mode or Stage3_6.current_mode or Stage3_8.current_mode or \
                    Stage3_9.current_mode or Stage3_10.current_mode or Stage3_11.current_mode:
                game_world.add_collision_pair('player_arrow:goblin_mob', self.player_arrow, None)
                # 기존 좀비 보스와 충돌 페어 추가
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'goblin_mob' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_arrow:goblin_mob', None, obj)

            if Stage3_7.current_mode:
                game_world.add_collision_pair('player_arrow:goblin_boss', self.player_arrow, None)
                for layer in game_world.world:
                    for obj in layer:
                        if hasattr(obj, 'handle_collision') and 'goblin_boss' in str(type(obj)).lower():
                            game_world.add_collision_pair('player_arrow:goblin_boss', None, obj)

    def exit(self, e):
        Player.is_attacking = False
        self.player.frame = 0

        self.player_sword = None
        self.player_arrow = None

    def do(self):
        if self.player.check_weapon() == 'none':
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
        if self.player.check_weapon() == 'sword':
            self.player.sword_image.clip_draw(int(self.player.frame) * 128, 128 * self.player.face_dir, 128, 128, self.player.x, self.player.y, 200, 200)
        elif self.player.check_weapon() == 'bow':
            self.player.bow_image.clip_draw(int(self.player.frame) * 64, 64 * self.player.face_dir, 64, 64,self.player.x, self.player.y, 100, 100)

class Player:
    walk_image = None
    idle_image = None
    dead_image = None
    sword_image = None
    combat_idle_image = None
    bow_image = None

    # 클래스 변수로 무기/방어구 ID 관리
    player_plate_id = 'none'
    player_bow_id = 'none'
    player_sword_id = 'normal_sword'
    current_weapon_id = player_sword_id

    is_attacking = False
    is_alive = True

    def load_walk_images(self):
        plate = Player.player_plate_id
        weapon = Player.current_weapon_id

        Player.walk_image = load_image(f'./image/player/{plate}/{weapon}/walk.png')
        self.walk_image = Player.walk_image

    def load_idle_images(self):
        plate = Player.player_plate_id
        weapon = Player.current_weapon_id

        Player.idle_image = load_image(f'./image/player/{plate}/{weapon}/idle.png')
        self.idle_image = Player.idle_image

    def load_dead_images(self):
        plate = Player.player_plate_id
        weapon = Player.current_weapon_id

        Player.dead_image = load_image(f'./image/player/{plate}/{weapon}/dead.png')
        self.dead_image = Player.dead_image

    def load_combat_idle_images(self):
        plate = Player.player_plate_id
        weapon = Player.current_weapon_id

        Player.combat_idle_image = load_image(f'./image/player/{plate}/{weapon}/combat_idle.png')
        self.combat_idle_image = Player.combat_idle_image

    def load_sword_images(self):
        plate = Player.player_plate_id
        weapon = Player.current_weapon_id

        Player.sword_image = load_image(f'./image/player/{plate}/{weapon}/sword_attack.png')
        self.sword_image = Player.sword_image

    def load_bow_images(self):
        plate = Player.player_plate_id
        weapon = Player.current_weapon_id

        Player.bow_image = load_image(f'./image/player/{plate}/{weapon}/bow_attack.png')
        self.bow_image = Player.bow_image

    def __init__(self):
        self.x = 510
        self.y = 160

        self.frame = 0

        self.dx = 0.0
        self.dy = 0.0

        self.xdir = 0 # up down direction (up: 1, down: -1, none: 0)
        self.ydir = 0 # left right direction (left: -1, right: 1, none: 0)

        self.face_dir = 0 # 마지막 방향 저장 (0: 오른쪽, 1: 아래, 2: 왼쪽, 3: 위)

        # 이동 검사 콜백: 모드가 주입
        self.move_validator = None

        # 데미지 관련
        self.last_damage_time = 0
        self.damage_cooldown = TIME_PER_ACTION * 1

        # 넉백 관련
        self.is_knocked_back = False
        self.knockback_distance = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

        # 이미지 로드
        self.load_walk_images()
        self.load_idle_images()
        self.load_dead_images()
        self.load_combat_idle_images()

        if self.check_weapon() == 'sword':
            self.load_sword_images()
        elif self.check_weapon() == 'bow':
            self.load_bow_images()

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
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        if not Player.is_alive:
            return 0, 0, 0, 0

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
        if not Player.is_alive:
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
            if space_down(('INPUT', event)):
                if not Stage1_0.stage1_0_create and not Stage2_0.stage2_0_create and not Stage3_0.stage3_0_create:
                    return
            self.state_machine.handle_state_event(('INPUT', event))

    def can_move_to(self, x, y):
        if callable(self.move_validator):
            return self.move_validator(x, y)

        return False

    def check_weapon(self):
        if Player.current_weapon_id in ['normal_sword', 'silver_sword', 'gold_sword']:
            return 'sword'
        elif Player.current_weapon_id in ['normal_bow', 'silver_bow', 'gold_bow']:
            return 'bow'
        else:
            return 'none'

    def handle_collision(self, group, other):
        global player_hp

        if group == 'player:coin':
            pass

        if group == 'player:slime_mob' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(10)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:slime_boss' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(20)
                self.apply_knockback(other, 30, 3.0)

        elif group == 'player:zombie_mob' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(10)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:zombie_mace' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(15)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:zombie_boss' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(15)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:zombie_boss_waraxe' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(25)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:goblin_mob' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(15)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:goblin_mace' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(20)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:goblin_arrow' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(20)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:goblin_boss' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(15)
                self.apply_knockback(other, 20, 1.0)

        elif group == 'player:goblin_boss_sword' and Player.is_alive:
            current_time = time.time()
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.apply_damage(40)
                self.apply_knockback(other, 20, 1.0)

    def apply_damage(self, base_damage):
        global player_hp

        # 방어구에 따른 데미지 배율 계산
        damage_multiplier = 1.0
        if Player.player_plate_id == 'normal_plate':
            damage_multiplier = 0.9
        elif Player.player_plate_id == 'silver_plate':
            damage_multiplier = 0.75
        elif Player.player_plate_id == 'gold_plate':
            damage_multiplier = 0.5

        # 실제 데미지 계산 및 적용
        actual_damage = int(base_damage * damage_multiplier)
        player_hp -= actual_damage
        self.last_damage_time = time.time()

        # HP가 0 이하로 떨어지면 사망 처리
        if player_hp <= 0:
            player_hp = 0
            sounds.player_dead_sound.play()
            Player.is_alive = False
            self.state_machine.handle_state_event(('DIE', None))
            # print("Player is dead!")
        else:
            if actual_damage <= 15:
                sounds.player_hurt_low_sound.play()
            else:
                sounds.player_hurt_high_sound.play()
            # print(f"Player damaged! HP: {player_hp} (took {actual_damage} damage)")

    def apply_knockback(self, other, distance, konck_dist):
        dx = self.x - other.x
        dy = self.y - other.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist > 0:
            nx = dx / dist
            ny = dy / dist

            self.is_knocked_back = True
            self.knockback_distance = distance
            self.knockback_dx = nx * konck_dist
            self.knockback_dy = ny * konck_dist