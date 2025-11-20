# game 내의 객체들의 생성과 소멸을 관리하는 모듈입니다.

# world[0] : 무조건 백그라운드 이미지
# world[1] : 백 오브젝트 이미지
# world[2] : 플레이어 오브젝트 이미지
# world[3] : 앞 오브젝트 이미지
# world[4] : UI 오브젝트
world = [[], [], [], [], []] # 게임 내 객체를 추가하는 함수

def add_object(o, depth = 0): # 게임 내 객체를 추가하는 함수
    world[depth].append(o)

def add_objects(ol, depth = 0): # 게임 내 객체들을 추가하는 함수
    world[depth] += ol

# 게임 월드의 모든 객체들을 업데이트
def update():
    for layer in world:
        for o in layer:
            o.update()

# 게임 월드의 모든 객체들을 그리기
def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

    raise ValueError('Cannot delete non existing object')


def clear():
    global world

    for layer in world:
        layer.clear()


def collide(a, b):
    # get_bb()가 None을 반환할 수 있으므로 체크
    bb_a = a.get_bb()
    bb_b = b.get_bb()

    # 둘 중 하나라도 None이면 충돌하지 않음
    if bb_a is None or bb_b is None:
        return False

    left_a, bottom_a, right_a, top_a = bb_a
    left_b, bottom_b, right_b, top_b = bb_b

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


collision_pairs = {}
def add_collision_pair(group, a, b):
    if group not in collision_pairs: # 처음 등록하는 그룹이면
        collision_pairs[group] = ([], []) # 해당 그룹에 대해서 초기화
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collsions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)