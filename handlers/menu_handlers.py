from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter

from database.database import users_db
from keyboards.keyboards import yes_no_kb, menu_kb
from lexicon.lexicon_ru import LEXICON_RU

from aiogram.fsm.context import FSMContext
from FSM.fsm import FSM_SET_NAME



router = Router()

# Хэндлер на команду "/start" - будет
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    if message.from_user.id in users_db:  # Если пользователь уже в базе
        await message.answer(text=f'Приветствую тебя, {users_db[message.from_user.id]}, я Небула - бот Молекулы\n\n'
                                  f'{LEXICON_RU["text_menu"]}',
                                  reply_markup=menu_kb)

    elif message.from_user.full_name:  # Если указан фулл нейм
        await message.answer(text=f'Приветствую тебя, {message.from_user.full_name}, я Небула - бот Молекулы\n\n'
                                   'Могу ли я к тебе так обращаться?', reply_markup=yes_no_kb)
        # если да то заносим имя в базу
        # если нет то устанавливаем машину состояний: ожидание ввода имени, пользователь указывает имя, далее заносим его в базу

    else:  # Если пользователя нет в базе и не указан фулл нейм
        await message.answer(text=LEXICON_RU['unknown'])
        # устанавливаем машину состояний: ожидание ввода имени, пользователь указывает имя, заносим в базу
        await state.set_state(FSM_SET_NAME.fill_name)