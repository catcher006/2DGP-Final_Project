from pico2d import load_image
from state_machine import StateMachine
from LocationManager import location_manager

class VillageBackObject:
    def __init__(self, bo):
        self.bo = bo
        self.image = load_image('deongeon_door.png')  # 집 문 오브젝트 이미지
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass

    def draw(self):
        # 마을에 있을 때만 던전 문 그리기
        if location_manager.is_village():
            self.image.clip_draw(0, 0, 122, 104, 529, 440)

class HouseBackObject:
    def __init__(self, bo):
        self.bo = bo
        # self.image = load_image('house_interior.png')  # 집 내부 배경

    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass

    def draw(self):
        if location_manager.is_house():
            # 집 내부 오브젝트들 그리기
            pass

class ShopBackObject:
    def __init__(self, bo):
        self.bo = bo
        # self.image = load_image('shop_interior.png')  # 상점 내부 배경

    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass

    def draw(self):
        if location_manager.is_shop():
            # 상점 내부 오브젝트들 그리기
            pass

class DungeonMainBackObject:
    def __init__(self, bo):
        self.bo = bo
        # self.image = load_image('dungeon_main.png')

    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass

    def draw(self):
        if location_manager.is_dungeon_main():
            # 던전 메인 오브젝트들 그리기
            pass

class DungeonInsideBackObject:
    def __init__(self, bo):
        self.bo = bo
        # self.image = load_image('dungeon_inside.png')

    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass

    def draw(self):
        if location_manager.is_dungeon_inside():
            # 던전 내부 오브젝트들 그리기
            pass

def to_village(e): return e == 'village'
def to_house(e): return e == 'house'
def to_shop(e): return e == 'shop'
def to_dungeon_main(e): return e == 'dungeon_main'
def to_dungeon_inside(e): return e == 'dungeon_inside'

class Back_Object:
    def __init__(self):
        self.VILLAGE = VillageBackObject(self)
        self.HOUSE = HouseBackObject(self)
        self.SHOP = ShopBackObject(self)
        self.DUNGEON_MAIN = DungeonMainBackObject(self)
        self.DUNGEON_INSIDE = DungeonInsideBackObject(self)

        self.state_machine = StateMachine(
            self.VILLAGE,
            {
                self.VILLAGE: {to_house: self.HOUSE, to_shop: self.SHOP, to_dungeon_main: self.DUNGEON_MAIN},
                self.HOUSE: {to_village: self.VILLAGE},
                self.SHOP: {to_village: self.VILLAGE},
                self.DUNGEON_MAIN: {to_village: self.VILLAGE, to_dungeon_inside: self.DUNGEON_INSIDE},
                self.DUNGEON_INSIDE: {to_dungeon_main: self.DUNGEON_MAIN}
            }
        )

    def set_location(self, location):
        # 위치 변경 시 location_manager와 state_machine 동기화
        location_manager.set_location(location)
        self.state_machine.handle_state_event(location)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()