from pico2d import load_image, get_time

class Village_Back_Object:
    def __init__(self):
        self.image = load_image('deongeon_door.png')  # 집 문 오브젝트 이미지

        # 문 애니메이션 관련
        self.door_animation_active = False
        self.door_frame = 0
        self.door_animation_time = 0
        self.door_max_frames = 8
        self.door_opened = False  # 문이 열린 상태 추적

    def enter(self, e): pass
    def exit(self, e): pass
    def update(self): pass

    def do(self):
        # 문 애니메이션 업데이트
        if self.door_animation_active:
            current_time = get_time()
            if current_time - self.door_animation_time > 0.1:
                self.door_frame += 1
                self.door_animation_time = current_time

                # 마지막 프레임 도달 시 애니메이션 종료
                if self.door_frame >= self.door_max_frames:
                    self.door_animation_active = False
                    self.door_opened = True
                    self.door_frame = 7  # 마지막 프레임에서 유지
                    print("Door animation finished!")

    def draw(self):
        self.image.clip_draw(self.door_frame * 122, 0, 122, 104, 529, 440)

    def activate_door_animation(self):
        # 문이 이미 열려있으면 애니메이션 실행하지 않음
        if not self.door_opened and not self.door_animation_active:
            self.door_animation_active = True
            self.door_frame = 0
            self.door_animation_time = get_time()
            print("Door animation started!")