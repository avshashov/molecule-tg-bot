from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import (
    LEXICON_SET_USER_NAME,
    LEXICON_MENU_BUTTONS,
    LEXICON_ABOUT_PROJECT,
    LEXICON_RENT,
    LEXICON_PICTURES
)

# ----------------------------------<УСТАНОВКИ ИМЕНИ ПОЛЬЗОВАТЕЛЯ>--------------------------------------------------

# Клавиатура с кнопками выбора ответа на вопрос как обращаться к пользователю
def yes_no_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_SET_USER_NAME['of_course'], callback_data='of_course'))
    kb.add(InlineKeyboardButton(text=LEXICON_SET_USER_NAME['another name'], callback_data='another name'))
    kb.adjust(2)
    return kb.as_markup()


# Клавиатура подтверждения имени
def yes_no_name_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_SET_USER_NAME['confirm'], callback_data='confirm'))
    kb.add(InlineKeyboardButton(text=LEXICON_SET_USER_NAME['not'], callback_data='not'))
    kb.adjust(2)
    return kb.as_markup()

# ----------------------------------<ГЛАВНОЕ МЕНЮ>--------------------------------------------------

# Клавиатура главного меню
def menu_kb() -> ReplyKeyboardMarkup:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text=LEXICON_MENU_BUTTONS['announcements'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['projects'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['rent'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['pictures'])
    menu_builder.button(text=LEXICON_MENU_BUTTONS['project'])
    menu_builder.adjust(2)
    return menu_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)

# ----------------------------------<БЛОК О ПРОЕКТЕ>--------------------------------------------------

# Клавиатура кнопки "О проекте"
def about_project() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_ABOUT_PROJECT['go_website'], url='https://t.me/Molecule_nebula_bot'
        )
    )
    kb.add(
        InlineKeyboardButton(
            text=LEXICON_ABOUT_PROJECT['download_presentation'], callback_data='download_presentation'
        )
    )
    kb.add(InlineKeyboardButton(text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'))
    kb.adjust(1)
    return kb.as_markup()

# ----------------------------------<БЛОК АРЕНДА>--------------------------------------------------

# Клавиатура кнопки "Аренда"
def rent() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['rental_request'], callback_data='rental_request'))
    kb.add(InlineKeyboardButton(text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'))
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура выбора способа связи
def communication_method() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['call'], callback_data='call'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['telegram'], callback_data='telegram'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['whatsapp'], callback_data='whatsapp'))
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура выбора количества залов
def how_room() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['one'], callback_data='one'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['two'], callback_data='two'))
    kb.adjust(2)
    return kb.as_markup()


# Клавиатура - кнопка 'Отправить' и кнопка 'Исправить'
def send() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['send'], callback_data='send'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['repeat_request'], callback_data='repeat_request'))
    kb.adjust(2)
    return kb.as_markup()


# Клавиатура - кнопка 'Оставить заявку'
def rental_request() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['rental_request'], callback_data='rental_request'))
    return kb.as_markup()


# Клавиатура - кнопка 'Отмена'
def cancel_rent() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['cancel_button'], callback_data='cancel_button'))
    return kb.as_markup()


# Клавиатура - кнопка 'Отправить контакт'
def send_contact() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=LEXICON_RENT['send_telephone'], request_contact=True)
    return kb.as_markup(resize_keyboard=True)

# ----------------------------------<БЛОК КАРТИНЫ>--------------------------------------------------

# Клавиатура кнопки "Картины"
def pictures() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_PICTURES['buy_ready'], callback_data='buy_ready'))
    kb.add(InlineKeyboardButton(text=LEXICON_PICTURES['order_painting'], callback_data='order_painting'))
    kb.row(*[InlineKeyboardButton(text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'),
            InlineKeyboardButton(text=LEXICON_PICTURES['online_gallery'], callback_data='online_gallery')],
            width=1)
    return kb.as_markup()


# Клавиатура кнопки "Купить готовую"
def buy_ready() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_PICTURES['catalog_paintings'], url='https://disk.yandex.ru/d/1MSKch2JtaetfA'))
    kb.add(InlineKeyboardButton(text=LEXICON_PICTURES['contact_me'], callback_data='contact_me'))
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура выбора способа связи
def method_contact() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['call'], callback_data='call'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['telegram'], callback_data='telegram'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['whatsapp'], callback_data='whatsapp'))
    kb.add(InlineKeyboardButton(text=LEXICON_PICTURES['email'], callback_data='email'))
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура - кнопка 'Отправить' и кнопка 'Исправить'
def send_correct() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['send'], callback_data='send_contact'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['repeat_request'], callback_data='correct'))
    kb.adjust(2)
    return kb.as_markup()
