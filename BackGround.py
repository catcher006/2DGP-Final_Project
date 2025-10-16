from pico2d import load_image


class Background:
    def __init__(self):
        self.backgrounds = {
            'village': load_image('village.png'),
        }

        # 현재 장소
        self.current_location = 'village'

    def update(self):
        # 배경 업데이트 로직 (현재는 빈 메서드)
        pass

    def draw(self):
        if self.current_location in self.backgrounds:
            self.backgrounds[self.current_location].draw_to_origin(0, 0, 1024, 576)
