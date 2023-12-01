from aiogram.fsm.state import default_state, State, StatesGroup

class FSM_SET_NAME(StatesGroup):
    enter_name = State()   # Состояние ожидания ввода имени