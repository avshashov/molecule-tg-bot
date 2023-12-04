from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU

# Клавиатура с кнопками выбора ответа на вопрос как обращаться к пользователю
def yes_no_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RU['of_course'], callback_data='of_course'))
    kb.add(InlineKeyboardButton(text=LEXICON_RU['another name'], callback_data='another name'))
    kb.adjust(2)
    return kb.as_markup()

# Клавиатура подтверждения имени
def yes_no_name_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=LEXICON_RU['confirm'], callback_data='confirm'))
    kb.add(InlineKeyboardButton(text=LEXICON_RU['not'], callback_data='not'))
    kb.adjust(2)
    return kb.as_markup()


# Клавиатура главного меню
def menu_kb() -> ReplyKeyboardMarkup:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text=LEXICON_RU['announcements'])
    menu_builder.button(text=LEXICON_RU['projects'])
    menu_builder.button(text=LEXICON_RU['rent'])
    menu_builder.button(text=LEXICON_RU['pictures'])
    menu_builder.button(text=LEXICON_RU['project'])
    menu_builder.adjust(2)

    return menu_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)