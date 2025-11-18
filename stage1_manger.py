# stage1 진행 상태 확인 전역 변수
stage1_in_game = False

# 각 방 생성 여부 전역 변수
stage1_0_create = None
stage1_1_create = None
stage1_2_create = None
stage1_3_create = None
stage1_4_create = None
stage1_5_create = None
stage1_6_create = None
stage1_7_create = None


def reset_stage1_manager():
    global stage1_0_create, stage1_1_create, stage1_2_create, stage1_3_create
    global stage1_4_create, stage1_5_create, stage1_6_create, stage1_7_create
    global stage1_in_game

    stage1_in_game = False

    stage1_0_create = None
    stage1_1_create = None
    stage1_2_create = None
    stage1_3_create = None
    stage1_4_create = None
    stage1_5_create = None
    stage1_6_create = None
    stage1_7_create = None