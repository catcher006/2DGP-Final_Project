from pico2d import load_image

class Village:
    def __init__(self):
        # 마을의 이동 가능 통로 정의
        self.paths = [
            {'type': 'rect', 'min_x': 10, 'max_x': 1014, 'min_y': 120, 'max_y': 190},  # 중앙 메인 통로 - 가로구역
            {'type': 'rect', 'min_x': 480, 'max_x': 590, 'min_y': 40, 'max_y': 380},  # 중앙 메인 통로 - 세로구역
            {'type': 'polygon', 'points': [
                (190, 190),  # 하단 왼쪽
                (270, 190),  # 하단 오른쪽
                (260, 210),  # 상단 오른쪽
                (210, 210)  # 상단 왼쪽
            ]},  # 집 입구 통로
            {'type': 'polygon', 'points': [
                (730, 190),  # 하단 왼쪽
                (800, 190),  # 하단 오른쪽
                (810, 220),  # 상단 오른쪽
                (770, 230)  # 상단 왼쪽
            ]}  # 상점 입구 통로
        ]

        self.image = load_image('./image/background/village.png')
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