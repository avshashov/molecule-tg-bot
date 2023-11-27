from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from database.database import users_db


router = Router()

# Хэндлер на команду "/start" - будет
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def start_command(message: Message):
    if message.from_user.id in users_db:
        await message.answer(text='Приветствую тебя, {users_db[message.from_user.id]}, я Небула - бот Молекулы')