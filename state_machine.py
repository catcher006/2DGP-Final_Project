from event_to_string import event_to_string
from pico2d import SDL_MOUSEMOTION

class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('START', None)) # 시작 상태로 진입

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event):
        # state_event가 어떤 이벤트인지 체크할 수 있어야 함
        for check_event in self.rules[self.cur_state].keys():
            if check_event(state_event):
                self.next_state = self.rules[self.cur_state][check_event]
                self.cur_state.exit(state_event)
                self.next_state.enter(state_event)
                self.next_state.enter(state_event)
                # 중요한 상태 변화만 출력
                if state_event[0] != 'INPUT':
                    print(
                        f"State Translation: {self.cur_state.__class__.__name__} -> {self.next_state.__class__.__name__} on event {event_to_string(state_event)}")
                self.cur_state = self.next_state
                return
        # 이벤트에 대한 처리가 안됐다. 따라서 문제가 발생
        # 마우스 이벤트는 출력하지 않음
        if state_event[0] == 'INPUT' and hasattr(state_event[1], 'type'):
            if state_event[1].type not in (SDL_MOUSEMOTION,):
                print(f"처리되지 않은 이벤트 {event_to_string(state_event)} 가 있습니다")