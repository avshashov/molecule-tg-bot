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
    send_rent = State() # Состояние готовности к отправке сообщения админам


class FSM_PICTURE(StatesGroup):
    how_contact_buy_ready = State()
    enter_telephone_buy_ready = State()
    enter_email_buy_ready = State()
    send = State()
    enter_telephone_order = State()
    enter_email_order = State()
    how_contact_order = State()
