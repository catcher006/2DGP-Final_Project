from pico2d import load_image
from state_machine import StateMachine

class VillageObject:
    def __init__(self, fo):
        self.fo = fo
        self.image = load_image('village_objects_2.png')
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass
    def draw(self):
        self.image.draw_to_origin(0, 0, 1024, 576)

def to_village(e): return e == 'village'

class Front_Object:
    def __init__(self):
        self.VILLAGE = VillageObject(self)

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