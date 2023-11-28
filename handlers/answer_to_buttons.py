from aiogram import F, Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from database.database import users_db

router = Router()
# Хендлер на кнопку "Конечно)" заносит пользователя в базу данных и выводит главное меню
@router.message(F.text == LEXICON_RU['of_course'])
async def of_course_answer(message: Message):
    await message.answer(text='Отлично)')
    users_db[message.from_user.id] = message.from_user.full_name
    #  Выводим главное меню