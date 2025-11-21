import time

frame_time = 0.0
running = None
stack = None

# 모드 객체에서 이름을 추출하는 함수
def _get_mode_name(mode):
    return getattr(mode, '__name__', str(mode))

def change_mode(mode, *args):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1]['mode'].finish()
        # remove the current mode
        stack.pop()

    entry = {'name': _get_mode_name(mode), 'mode': mode}
    stack.append(entry)
    mode.init(*args)

def push_mode(mode, *args):
    global stack
    if len(stack) > 0:
        stack[-1]['mode'].pause()

    entry = {'name': _get_mode_name(mode), 'mode': mode}
    stack.append(entry)
    mode.init(*args)

def pop_mode(target_mode=None, *args):
    global stack
    if not stack:
        return

    # 타겟 없이 호출하면 최상단 pop (기본 동작)
    if target_mode is None:
        stack[-1]['mode'].finish()
        stack.pop()

        if stack:
            stack[-1]['mode'].resume()
            return

    # 타겟 모드가 지정된 경우
    target_name = _get_mode_name(target_mode)

    # 스택에서 타겟 모드 찾기
    found_idx = -1
    for i, entry in enumerate(stack):
        if entry['name'] == target_name:
            found_idx = i
            break

    if found_idx == -1:
        print(f"Warning: Target mode {target_name} not found in stack")
        return

    # 이미 최상단이면 아무것도 안 함
    if found_idx == len(stack) - 1:
        return

    # 현재 최상단 모드 pause
    stack[-1]['mode'].pause()

    # 타겟 모드를 스택에서 제거 (위치는 유지)
    target_entry = stack.pop(found_idx)

    # 타겟 모드를 최상단에 추가
    stack.append(target_entry)

    # 타겟 모드 resume
    stack[-1]['mode'].resume(*args)

    print(f"Moved target mode {target_name} to top, stack depth: {len(stack)}")

def quit():
    global running
    running = False

def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = []

    entry = {'name': _get_mode_name(start_mode), 'mode': start_mode}
    stack.append(entry)
    start_mode.init()

    frame_time = 0.0
    current_time = time.time()  # 현재 시간 기록

    while running:
        stack[-1]['mode'].handle_events()
        stack[-1]['mode'].update()
        stack[-1]['mode'].draw()

        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time = time.time()
        # print(f'Frame Time: {frame_time:.4f}, Frame Rate: {frame_rate:.2f} FPS')

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1]['mode'].finish()
        stack.pop()

def clear_stage1_modes(*args):
    global stack
    stage_mode_names = {
        'stage1_0_mode', 'stage1_1_mode', 'stage1_2_mode', 'stage1_3_mode',
        'stage1_4_mode', 'stage1_5_mode', 'stage1_6_mode', 'stage1_7_mode'
    }

    print(f"Before clear: stack depth = {len(stack)}")
    for entry in stack:
        print(f"  - {entry['name']}")

    # 제거할 모드들의 finish() 먼저 호출
    for entry in stack:
        if entry['name'] in stage_mode_names:
            print(f"Finishing {entry['name']}")
            entry['mode'].finish()

    # 스테이지 모드가 아닌 것만 남기기
    stack = [entry for entry in stack if entry['name'] not in stage_mode_names]

    print(f"After clear: stack depth = {len(stack)}")
    for entry in stack:
        print(f"  - {entry['name']}")

    # 던전 메인이 남아있으면 resume 호출 (인자 전달)
    if stack and stack[-1]['name'] == 'dungeonmain_mode':
        print("Resuming dungeonmain_mode with args")
        if args:
            stack[-1]['mode'].resume(*args)
        else:
            stack[-1]['mode'].resume()