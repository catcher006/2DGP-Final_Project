from pico2d import *

class Village_Front_Object:
    def __init__(self):
        self.image = load_image('village_objects_2.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw_to_origin(0, 0, 1024, 576)