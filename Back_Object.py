from pico2d import load_image
from state_machine import StateMachine

class VillageBackObject:
    def __init__(self, bo):
        self.bo = bo
        self.image = load_image('deongeon_door.png')  # 집 문 오브젝트 이미지
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass
    def draw(self):
        self.image.clip_draw(0, 0, 122, 104, 529, 440)

def to_village(e): return e == 'village'

class Back_Object:
    def __init__(self):
        self.VILLAGE = VillageBackObject(self)

        self.state_machine = StateMachine(
            self.VILLAGE,
            {
                self.VILLAGE: {}
            }
        )

    def set_location(self, location):
        self.state_machine.handle_state_event(location)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()