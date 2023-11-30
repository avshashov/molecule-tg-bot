from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU

# Клавиатура с кнопками выбора ответа на вопрос как обращаться к пользователю
yes = InlineKeyboardButton(text=LEXICON_RU['of_course'], callback_data='of_course')
no = InlineKeyboardButton(text=LEXICON_RU['another name'], callback_data='another name')

yes_no_kb = InlineKeyboardMarkup(
    inline_keyboard=[[yes, no]],)


# Клавиатура главного меню
announcements = KeyboardButton(text=LEXICON_RU['announcements'])
events_button = KeyboardButton(text=LEXICON_RU['projects'])
rent_button = KeyboardButton(text=LEXICON_RU['rent'])
pictures_button = KeyboardButton(text=LEXICON_RU['pictures'])
project_button = KeyboardButton(text=LEXICON_RU['project'])

menu_builder = ReplyKeyboardBuilder()

menu_builder.row(announcements, events_button, rent_button, pictures_button, project_button, width=2)

menu_kb: ReplyKeyboardMarkup = menu_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)