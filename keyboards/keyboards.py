from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU

# Клавиатура с кнопками выбора ответа на вопрос как обращаться к пользователю
def yes_no_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    yes = InlineKeyboardButton(text=LEXICON_RU['of_course'], callback_data='of_course')
    no = InlineKeyboardButton(text=LEXICON_RU['another name'], callback_data='another name')
    kb.row(yes, no, width=2)
    return kb.as_markup()

# Клавиатура подтверждения имени
def yes_no_name_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    yes_name = InlineKeyboardButton(text=LEXICON_RU['confirm'], callback_data='confirm')
    no_name = InlineKeyboardButton(text=LEXICON_RU['replace'], callback_data='replace')
    kb.row(yes_name, no_name, width=2)
    return kb.as_markup()


# Клавиатура главного меню
def menu_kb() -> ReplyKeyboardMarkup:
    menu_builder = ReplyKeyboardBuilder()
    announcements = KeyboardButton(text=LEXICON_RU['announcements'])
    events_button = KeyboardButton(text=LEXICON_RU['projects'])
    rent_button = KeyboardButton(text=LEXICON_RU['rent'])
    pictures_button = KeyboardButton(text=LEXICON_RU['pictures'])
    project_button = KeyboardButton(text=LEXICON_RU['project'])
    menu_builder.row(announcements, events_button, rent_button, pictures_button, project_button, width=2)

    return menu_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)