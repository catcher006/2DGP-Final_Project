from pico2d import load_image


class Front_Object:
    def __init__(self):
        self.front_objects = {
            'village': load_image('village_objects.png')  # 표지판 이미지
        }

        # 현재 장소
        self.current_location = 'village'


    def update(self):
        # 배경 업데이트 로직 (현재는 빈 메서드)
        pass

    def draw(self):
        if self.current_location in self.front_objects:
            self.front_objects[self.current_location].draw_to_origin(0, 0, 1024, 576)
