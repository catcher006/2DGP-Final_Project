# 각 방 생성 여부 전역 변수
stage1_0_create = None
stage1_1_create = None
stage1_2_create = None
stage1_3_create = None
stage1_4_create = None
stage1_5_create = None
stage1_6_create = None
stage1_7_create = None

# 각 방 마지막 몹 상태 전역 변수 (리스트 형태로 몹의 dict 저장)
stage1_0_mobs = None
stage1_1_mobs = None
stage1_2_mobs = None
stage1_3_mobs = None
stage1_4_mobs = None
stage1_5_mobs = None
stage1_6_mobs = None
stage1_7_mobs = None

# 각 방 마지막 몹 좌표 전역 변수
stage1_0_last_mob1_pos = None
stage1_0_last_mob2_pos = None
stage1_1_last_mob1_pos = None
stage1_1_last_mob2_pos = None
stage1_2_last_mob1_pos = None
stage1_2_last_mob2_pos = None
stage1_3_last_mob1_pos = None
stage1_3_last_mob2_pos = None
stage1_4_last_mob1_pos = None
stage1_4_last_mob2_pos = None
stage1_5_last_mob1_pos = None
stage1_5_last_mob2_pos = None
stage1_6_last_mob1_pos = None
stage1_6_last_mob2_pos = None
stage1_7_last_mob1_pos = None
stage1_7_last_mob2_pos = None

def reset_stage1_manager():
    global stage1_0_create, stage1_1_create, stage1_2_create, stage1_3_create
    global stage1_4_create, stage1_5_create, stage1_6_create, stage1_7_create
    global stage1_0_last_player_pos, stage1_1_last_player_pos, stage1_2_last_player_pos
    global stage1_3_last_player_pos, stage1_4_last_player_pos, stage1_5_last_player_pos
    global stage1_6_last_player_pos, stage1_7_last_player_pos
    global stage1_0_last_mob1_pos, stage1_0_last_mob2_pos
    global stage1_1_last_mob1_pos, stage1_1_last_mob2_pos
    global stage1_2_last_mob1_pos, stage1_2_last_mob2_pos
    global stage1_3_last_mob1_pos, stage1_3_last_mob2_pos
    global stage1_4_last_mob1_pos, stage1_4_last_mob2_pos
    global stage1_5_last_mob1_pos, stage1_5_last_mob2_pos
    global stage1_6_last_mob1_pos, stage1_6_last_mob2_pos
    global stage1_7_last_mob1_pos, stage1_7_last_mob2_pos

    stage1_0_create = None
    stage1_1_create = None
    stage1_2_create = None
    stage1_3_create = None
    stage1_4_create = None
    stage1_5_create = None
    stage1_6_create = None
    stage1_7_create = None

    stage1_0_last_mob1_pos = None
    stage1_0_last_mob2_pos = None
    stage1_1_last_mob1_pos = None
    stage1_1_last_mob2_pos = None
    stage1_2_last_mob1_pos = None
    stage1_2_last_mob2_pos = None
    stage1_3_last_mob1_pos = None
    stage1_3_last_mob2_pos = None
    stage1_4_last_mob1_pos = None
    stage1_4_last_mob2_pos = None
    stage1_5_last_mob1_pos = None
    stage1_5_last_mob2_pos = None
    stage1_6_last_mob1_pos = None
    stage1_6_last_mob2_pos = None
    stage1_7_last_mob1_pos = None
    stage1_7_last_mob2_pos = None

    stage1_0_mobs = None
    stage1_1_mobs = None
    stage1_2_mobs = None
    stage1_3_mobs = None
    stage1_4_mobs = None
    stage1_5_mobs = None
    stage1_6_mobs = None
    stage1_7_mobs = None


def stage1_0_slime_mobs():
    return stage1_0_mobs

def stage1_1_slime_mobs():
    return stage1_1_mobs

def stage1_2_slime_mobs():
    return stage1_2_mobs

def stage1_3_slime_mobs():
    return stage1_3_mobs

def stage1_4_slime_mobs():
    return stage1_4_mobs

def stage1_5_slime_mobs():
    return stage1_5_mobs

def stage1_6_slime_mobs():
    return stage1_6_mobs

def stage1_7_slime_mobs():
    return stage1_7_mobs