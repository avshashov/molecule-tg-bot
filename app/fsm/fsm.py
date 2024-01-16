from aiogram.fsm.state import State, StatesGroup


class FSMSetName(StatesGroup):
    enter_name = State()


class FSMRent(StatesGroup):
    enter_telephone = State()
    how_contact = State()
    date = State()
    event = State()
    how_people = State()
    send_rent = State()  # Состояние готовности к отправке сообщения админам


class FSMPicture(StatesGroup):
    how_contact_buy_ready = State()
    enter_telephone_buy_ready = State()
    enter_email_buy_ready = State()
    send_buy_ready = State()
    send_order = State()
    enter_telephone_order = State()
    enter_email_order = State()
    how_contact_order = State()
    for_whom = State()
    event = State()
    size = State()
    mood = State()
    color = State()


class FSMAdminRent(StatesGroup):
    enter_photo_title = State()
    enter_new_photo_title = State()
    enter_photo_description = State()
    enter_new_rent_text = State()
    open_photo = State()
    send_rent_photo = State()


class FSMAdminAboutProject(StatesGroup):
    upload_presentation = State()


class FSMAdminPicture(StatesGroup):
    upload_picture = State()
    enter_picture_title = State()
    enter_picture_description = State()
    enter_new_picture_title = State()
    enter_new_picture_description = State()
    open_picture = State()


class FSMAdminContacts(StatesGroup):
    enter_contacts = State()
