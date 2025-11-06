from pico2d import load_image

class Stage1:
    def __init__(self):
        self.paths = [
            {'type': 'rect', 'min_x': 105, 'max_x': 940, 'min_y': 85, 'max_y': 540},  # 기본 이동 구역
        ]

        self.room_number = 0
        self.max_room_number = 7
        self.image = load_image("./image/background/stage1/%d.png" % self.room_number)
    def enter(self, e): pass
    def exit(self, e): pass
    def do(self): pass
    def draw(self):
        self.image.draw_to_origin(0, 0, 1024, 576)
    def update(self): pass

    def _point_in_polygon(self, x, y, polygon):
        n = len(polygon)
        inside = False
        j = n - 1
        for i in range(n):
            if ((polygon[i][1] > y) != (polygon[j][1] > y)) and \
               (x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
                inside = not inside
            j = i
        return inside

    def is_walkable(self, x, y):
        for p in self.paths:
            if p.get('type') == 'rect':
                if p['min_x'] <= x <= p['max_x'] and p['min_y'] <= y <= p['max_y']:
                    return True
            elif p.get('type') == 'polygon':
                if self._point_in_polygon(x, y, p['points']):
                    return True
        return False

    def set_room(self, room_number):
        if 0 <= room_number <= self.max_room_number:
            self.room_number = room_number

