from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RU
from database.database import users_db
from keyboards.keyboards import menu_kb, yes_no_name_kb

from aiogram.fsm.context import FSMContext
from fsm.fsm import FSM_SET_NAME

router = Router()
# Хендлер на кнопку "Конечно)" заносит пользователя в базу данных и выводит главное меню
@router.callback_query(F.data == 'of_course')
async def of_course_answer(callback: CallbackQuery):
    users_db[callback.from_user.id] = callback.from_user.full_name
    await callback.message.edit_text(text='Отлично)\n\n')
    await callback.message.answer(text=f'{LEXICON_RU["text_menu"]}', reply_markup=menu_kb())


# Хендлер на кнопку "Изменить имя" устанавливает машину состояний: ожидание ввода имени
@router.callback_query(F.data == 'another name')
async def another_name_answer(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['your_name'])
    await callback.answer()
    await state.set_state(FSM_SET_NAME.enter_name)


#Хендлер на введенное имя (любое) сразу заносит имя в базу, приветствует, предлагает меню
@router.message(StateFilter(FSM_SET_NAME.enter_name))
async def name_sent(message: Message, state: FSMContext):
    await message.answer(text=f'Оставим это имя "{message.text}" ?', reply_markup=yes_no_name_kb())


    # Разделить хендлер на 2: кнопки ДА и НЕТ


#    await message.answer(text=f'Приветствую тебя, {message.text}!\n\n'
#                              f'{LEXICON_RU["text_menu"]}',
#                             reply_markup=menu_kb)

# Хендлер на кнопку ДА (подтверддение имени) - заносит имя в базу, приветствует, предлагает меню
@router.callback_query(F.data == 'confirm', StateFilter(FSM_SET_NAME.enter_name))
async def confirm(callback: CallbackQuery, state: FSMContext):
    users_db[callback.from_user.id] = callback.message.text # ИМЯ в базу через хранилище
    await state.clear()
    await callback.message.answer(text=f'Приветствую тебя, {callback.message.text}!\n\n'
                                       f'{LEXICON_RU["text_menu"]}',
                                       reply_markup=menu_kb())