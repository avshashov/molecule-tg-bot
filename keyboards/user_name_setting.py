from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import (
    LEXICON_SET_USER_NAME,
)


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