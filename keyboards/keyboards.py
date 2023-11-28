from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU

# Клавиатура с кнопками выбора ответа на вопрос как обращаться к пользователю
yes = KeyboardButton(text=LEXICON_RU['of_course'])
no = KeyboardButton(text=LEXICON_RU['another name'])

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[[yes, no]],
    resize_keyboard=True,
    one_time_keyboard=True)