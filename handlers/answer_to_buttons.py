from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from database.database import users_db
from keyboards.keyboards import menu_kb

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from FSM.fsm import FSM_SET_NAME

router = Router()
# Хендлер на кнопку "Конечно)" заносит пользователя в базу данных и выводит главное меню
@router.message(F.text == LEXICON_RU['of_course'])
async def of_course_answer(message: Message):
    users_db[message.from_user.id] = message.from_user.full_name
    await message.answer(text='Отлично)\n\n'
                               f'{LEXICON_RU["text_menu"]}',
                               reply_markup=menu_kb)


# Хендлер на кнопку "Нет, зови меня лучше так:" устанавливает машину состояний: ожидание ввода имени
@router.message(F.text == LEXICON_RU['another name'])
async def another_name_answer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['your_name'])
    await state.set_state(FSM_SET_NAME.fill_name)


# Хендлер на введенное имя (любое) сразу заносит имя в базу, приветствует, предлагает меню
@router.message(StateFilter(FSM_SET_NAME.fill_name))
async def name_sent(message: Message, state: FSMContext):
    users_db[message.from_user.id] = message.text
    await state.clear()
    await message.answer(text=f'Приветствую тебя, {message.text}!\n\n'
                              f'{LEXICON_RU["text_menu"]}',
                               reply_markup=menu_kb)
