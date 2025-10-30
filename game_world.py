# game 내의 객체들의 생성과 소멸을 관리하는 모듈입니다.

# world[0] : 무조건 백그라운드 이미지
# world[1] : 백 오브젝트 이미지
# world[2] : 플레이어 오브젝트 이미지
# world[3] : 앞 오브젝트 이미지
world = [[], [], [], []] # 게임 내 객체를 추가하는 함수

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

def remove_object(o): # 게임 내 객체를 제거하는 함수
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    raise ValueError("월드에 존재하지 않는 객체를 삭제하려고 합니다")

def clear():
    for layer in world:
        layer.clear()