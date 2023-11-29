from aiogram.fsm.state import default_state, State, StatesGroup

class FSM_SET_NAME(StatesGroup):
    fill_name = State()   # Состояние ожидания ввода имени