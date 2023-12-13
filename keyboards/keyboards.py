from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_SET_USER_NAME, LEXICON_MENU_BUTTONS, LEXICON_ABOUT_PROJECT, LEXICON_RENT


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


# Клавиатура кнопки "Аренда"
def rent() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['rental_request'], callback_data='rental_request'))
    kb.add(InlineKeyboardButton(text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'))
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура выбора способа связи (блок Аренда)
def communication_method() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['call'], callback_data='call'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['telegram'], callback_data='telegram'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['whatsapp'], callback_data='whatsapp'))
    kb.adjust(1)
    return kb.as_markup()


# Клавиатура выбора количества залов (блок Аренда)
def how_room() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['one'], callback_data='one'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['two'], callback_data='two'))
    kb.adjust(2)
    return kb.as_markup()


# Клавиатура - кнопка 'Отправить'(блок Аренда)
def send() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['send'], callback_data='send'))
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['rental_request'], callback_data='rental_request'))
    kb.adjust(2)
    return kb.as_markup()