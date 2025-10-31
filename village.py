from pico2d import load_image

class Village:
    def __init__(self):
        self.image = load_image('village_2.png')
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass
    def draw(self):
        self.image.draw_to_origin(0, 0, 1024, 576)
    def update(self): pass