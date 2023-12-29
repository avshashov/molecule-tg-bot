from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.lexicon.lexicon_ru import (
    LEXICON_MENU_BUTTONS,
    LEXICON_RENT,
)


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


# Клавиатура - кнопка 'Оставить заявку' и 'Главное меню'
def rental_request() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RENT['rental_request'], callback_data='rental_request'))
    kb.add(InlineKeyboardButton(text=LEXICON_MENU_BUTTONS['main_menu'], callback_data='main_menu'))
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
