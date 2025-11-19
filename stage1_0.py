from pico2d import load_image

class Stage1_0:
    def __init__(self):
        self.paths = [
            {'type': 'rect', 'min_x': 105, 'max_x': 940, 'min_y': 85, 'max_y': 540},  # 기본 이동 구역
            {'type': 'rect', 'min_x': 500, 'max_x': 550, 'min_y': 540, 'max_y': 600},  # 위쪽 문
            {'type': 'rect', 'min_x': 940, 'max_x': 1010, 'min_y': 270, 'max_y': 370},  # 우측 문
            {'type': 'rect', 'min_x': 500, 'max_x': 550, 'min_y': 0, 'max_y': 85},  # 아래쪽 문
        ]

        self.mob_paths = [
            {'type': 'rect', 'min_x': 105, 'max_x': 940, 'min_y': 85, 'max_y': 540},  # 기본 이동 구역
        ]

        self.image = load_image("./image/background/stage1/0.png")
        self.saved_mobs = [] # 몹 상태 저장용 리스트
        self.is_created = False # 방 생성 여부 플래그

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

    def is_mob_walkable(self, x, y):
        for p in self.mob_paths:
            if p.get('type') == 'rect':
                if p['min_x'] <= x <= p['max_x'] and p['min_y'] <= y <= p['max_y']:
                    return True
            elif p.get('type') == 'polygon':
                if self._point_in_polygon(x, y, p['points']):
                    return True
        return False

    # alive한 몹들의 직렬화된 상태를 저장
    def save_mobs(self, mobs):
        alive = []
        for m in mobs:
            if getattr(m, "is_alive", False):
                alive.append({
                    "type": getattr(m, "mob_type", None),
                    "x": getattr(m, "x", 0),
                    "y": getattr(m, "y", 0),
                    "hp": getattr(m, "hp", 0),
                    "frame": getattr(m, "frame", 0)
                })
        self.saved_mobs = alive

    def has_saved_mobs(self):
        return bool(self.saved_mobs)

    # 저장된 몹 데이터 리스트를 반환 (복원 담당 로직은 모드에서 수행)
    def restore_mobs_data(self):
        return list(self.saved_mobs)

    def clear_saved_mobs(self):
        self.saved_mobs = []