from pico2d import load_image


class Back_Object:
    def __init__(self):
        self.back_objects = {
            'village': load_image('village_home_door.png')  # 집 문 오브젝트 이미지
        }
        # 현재 장소
        self.current_location = 'village'


    def update(self):
        # 배경 업데이트 로직 (현재는 빈 메서드)
        pass

    def draw(self):
        if self.current_location in self.back_objects:
            self.back_objects[self.current_location].clip_draw(0 * 1024, 1024 * 0, 1024, 1024, 182, 262, 100, 80)
