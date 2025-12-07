import json
import os

# 기본 무기 데이터
DEFAULT_WEAPON_DATA = {
    'player_plate_id': 'none',
    'player_sword_id': 'normal_sword',
    'player_bow_id': 'none',
    'current_weapon_id': 'normal_sword'
}

# 기본 플레이어 데이터
DEFAULT_PLAYER_DATA = {
    'hp': 100,
    'coins': 500
}

WEAPON_SAVE_PATH = 'weapon_data.json'
PLAYER_SAVE_PATH = 'player_data.json'

class GameData:
    weapon_data = None
    player_data = None

    @staticmethod
    def initialize():
        """게임 시작 시 데이터 로드"""
        # 무기 데이터 로드
        if os.path.exists(WEAPON_SAVE_PATH):
            GameData.load_weapon()
        else:
            GameData.weapon_data = DEFAULT_WEAPON_DATA.copy()
            GameData.save_weapon()

        # 플레이어 데이터 로드
        if os.path.exists(PLAYER_SAVE_PATH):
            GameData.load_player()
        else:
            GameData.player_data = DEFAULT_PLAYER_DATA.copy()
            GameData.save_player()

    @staticmethod
    def save_weapon():
        """무기 데이터 저장"""
        try:
            with open(WEAPON_SAVE_PATH, 'w', encoding='utf-8') as f:
                json.dump(GameData.weapon_data, f, indent=4, ensure_ascii=False)
            print("Weapon data saved!")
        except Exception as e:
            print(f"Failed to save weapon data: {e}")

    @staticmethod
    def load_weapon():
        """무기 데이터 로드"""
        try:
            with open(WEAPON_SAVE_PATH, 'r', encoding='utf-8') as f:
                GameData.weapon_data = json.load(f)
            print("Weapon data loaded!")
        except Exception as e:
            print(f"Failed to load weapon data: {e}")
            GameData.weapon_data = DEFAULT_WEAPON_DATA.copy()

    @staticmethod
    def save_player():
        """플레이어 데이터(HP, 코인) 저장"""
        try:
            with open(PLAYER_SAVE_PATH, 'w', encoding='utf-8') as f:
                json.dump(GameData.player_data, f, indent=4, ensure_ascii=False)
            print("Player data saved!")
        except Exception as e:
            print(f"Failed to save player data: {e}")

    @staticmethod
    def load_player():
        """플레이어 데이터(HP, 코인) 로드"""
        try:
            with open(PLAYER_SAVE_PATH, 'r', encoding='utf-8') as f:
                GameData.player_data = json.load(f)
            print("Player data loaded!")
        except Exception as e:
            print(f"Failed to load player data: {e}")
            GameData.player_data = DEFAULT_PLAYER_DATA.copy()

    @staticmethod
    def update_weapon():
        """현재 무기 상태를 데이터에 반영하고 저장"""
        from player import Player

        GameData.weapon_data['player_plate_id'] = Player.player_plate_id
        GameData.weapon_data['player_sword_id'] = Player.player_sword_id
        GameData.weapon_data['player_bow_id'] = Player.player_bow_id
        GameData.weapon_data['current_weapon_id'] = Player.current_weapon_id

        GameData.save_weapon()

    @staticmethod
    def update_player():
        """현재 플레이어 상태(HP, 코인)를 데이터에 반영하고 저장"""
        from player import player_hp

        GameData.player_data['hp'] = player_hp

        GameData.save_player()

    @staticmethod
    def apply_weapon():
        """저장된 무기 데이터를 게임에 적용"""
        from player import Player

        Player.player_plate_id = GameData.weapon_data['player_plate_id']
        Player.player_sword_id = GameData.weapon_data['player_sword_id']
        Player.player_bow_id = GameData.weapon_data['player_bow_id']
        Player.current_weapon_id = GameData.weapon_data['current_weapon_id']

    @staticmethod
    def apply_player():
        """저장된 플레이어 데이터(HP, 코인)를 게임에 적용"""
        import player as player_module

        player_module.player_hp = GameData.player_data['hp']

    @staticmethod
    def add_coins(amount):
        """코인 추가 및 저장"""
        GameData.player_data['coins'] += amount
        GameData.save_player()

    @staticmethod
    def get_coins():
        """현재 코인 수 반환"""
        return GameData.player_data['coins']

    @staticmethod
    def reset_weapon():
        """무기 데이터 초기화"""
        GameData.weapon_data = DEFAULT_WEAPON_DATA.copy()
        GameData.save_weapon()

    @staticmethod
    def reset_player():
        """플레이어 데이터 초기화"""
        GameData.player_data = DEFAULT_PLAYER_DATA.copy()
        GameData.save_player()

    @staticmethod
    def reset_all():
        """모든 데이터 초기화"""
        GameData.reset_weapon()
        GameData.reset_player()
