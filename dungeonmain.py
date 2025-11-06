from pico2d import load_image

class Dungeonmain:
    def __init__(self):
        self.paths = [
            {'type': 'rect', 'min_x': 70, 'max_x': 895, 'min_y': 60, 'max_y': 220},  # 기본 아래 구역1
            {'type': 'rect', 'min_x': 895, 'max_x': 1000, 'min_y': 60, 'max_y': 210},  # 기본 아래 구역2
            {'type': 'rect', 'min_x': 115, 'max_x': 880, 'min_y': 200, 'max_y': 280},  # 좌측 돌부리 - 우측 용암
            {'type': 'rect', 'min_x': 115, 'max_x': 290, 'min_y': 200, 'max_y': 310},  # 좌측 돌부리 - 중앙 나무 판자
            {'type': 'rect', 'min_x': 380, 'max_x': 930, 'min_y': 280, 'max_y': 330},  # 좌측 돌부리 - 우측 용암
            {'type': 'rect', 'min_x': 195, 'max_x': 290, 'min_y': 310, 'max_y': 400},  # 1번 문
            {'type': 'rect', 'min_x': 505, 'max_x': 585, 'min_y': 330, 'max_y': 400},  # 2번 문
            {'type': 'rect', 'min_x': 780, 'max_x': 880, 'min_y': 330, 'max_y': 400},  # 3번 문
        ]

        self.image = load_image('./image/background/dungeon_main.png')
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