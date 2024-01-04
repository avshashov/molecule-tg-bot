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
    send_rent = State()  # Состояние готовности к отправке сообщения админам


class FSM_PICTURE(StatesGroup):
    how_contact_buy_ready = State()
    enter_telephone_buy_ready = State()
    enter_email_buy_ready = State()

    send_buy_ready = State()
    send_order = State()

    enter_telephone_order = State()
    enter_email_order = State()
    how_contact_order = State()

    for_whom = State()  # Для кого картина
    event = State()  # По какому случаю
    size = State()  # Какого размера
    mood = State()  # Какое настроение
    color = State()  # Цветовая гамма


class FSMAdminRent(StatesGroup):
    enter_photo_title = State()
    enter_new_photo_title = State()
    enter_photo_description = State()
    enter_new_rent_text = State()
    open_photo = State()
    send_rent_photo = State()


class FSMAdminAboutProject(StatesGroup):
    upload_presentation = State()
