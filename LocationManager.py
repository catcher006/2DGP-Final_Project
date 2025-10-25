class LocationManager:
    def __init__(self):
        self.current_location = 'village'  # 기본 위치는 마을

    def set_location(self, location):
        # 현재 위치 설정
        valid_locations = ['village', 'house', 'shop', 'dungeon_main', 'dungeon_inside']
        if location in valid_locations:
            self.current_location = location
            print(f"Location changed to: {location}")
        else:
            print(f"Invalid location: {location}")

    def get_location(self):
        # 현재 위치 반환
        return self.current_location

    def is_village(self):
        # 마을에 있는지 확인
        return self.current_location == 'village'

    def is_house(self):
        # 집에 있는지 확인
        return self.current_location == 'house'

    def is_shop(self):
        # 상점에 있는지 확인
        return self.current_location == 'shop'

    def is_dungeon_main(self):
        # 던전 메인에 있는지 확인
        return self.current_location == 'dungeon_main'

    def is_dungeon_inside(self):
        # 던전 내부에 있는지 확인
        return self.current_location == 'dungeon_inside'


# 전역 위치 매니저 인스턴스
location_manager = LocationManager()