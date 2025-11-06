from pico2d import load_image

class Stage1:
    def __init__(self):
        self.room_number = 0
        self.max_room_number = 7
        self.image = load_image("./image/background/stage1/%d.png" % self.room_number)
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass
    def draw(self):
        self.image.draw_to_origin(0, 0, 1024, 576)
    def update(self): pass