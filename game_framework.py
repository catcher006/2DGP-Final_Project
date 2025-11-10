import time

frame_time = 0.0
running = None
stack = None

def _ensure_initialized_flag(mode):
    if not hasattr(mode, "initialized"):
        mode.initialized = False


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    _ensure_initialized_flag(mode)
    stack.append(mode)
    mode.init()
    mode.initialized = True


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    _ensure_initialized_flag(mode)
    stack.append(mode)
    # 이미 init 된 모드면 resume, 아니면 init 실행
    if mode.initialized:
        if hasattr(mode, "resume"):
            mode.resume()
        else:
            mode.init()
            mode.initialized = True


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        _ensure_initialized_flag(stack[-1])
        # 이전 모드는 이미 초기화되어 있어야 하므로 resume 실행
        if stack[-1].initialized:
            if hasattr(stack[-1], "resume"):
                stack[-1].resume()
            else:
                # 안전 장치: 초기화가 안된 상태면 init만 한 번 실행
                stack[-1].init()
                stack[-1].initialized = True


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = []
    _ensure_initialized_flag(start_mode)
    stack.append(start_mode)

    if start_mode.initialized:
        if hasattr(start_mode, "resume"):
            start_mode.resume()
    else:
        start_mode.init()
        start_mode.initialized = True

    global frame_time
    frame_time = 0.0
    current_time = time.time()  # 현재 시간 기록

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time = time.time()
        # print(f'Frame Time: {frame_time:.4f}, Frame Rate: {frame_rate:.2f} FPS')

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()