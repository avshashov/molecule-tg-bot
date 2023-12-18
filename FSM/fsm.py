from aiogram.fsm.state import State, StatesGroup


class FSM_SET_NAME(StatesGroup):
    enter_name = State()  # Состояние ожидания ввода имени


class FSM_RENT(StatesGroup):  # Состояние пользователя:
    enter_telephone = State()  # Ввод телефона
    how_contact = State()  # Как связаться
    date = State()  # Ввод даты
    event = State()  # Какое мероприятие
    how_people = State()  # Сколько человек
    how_room = State()  # Сколько залов (1 или 2)


class FSM_PICTURE(StatesGroup):
    how_contact = State()
    enter_telephone = State()
