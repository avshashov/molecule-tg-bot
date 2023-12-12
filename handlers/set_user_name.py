from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_SET_USER_NAME, LEXICON_MENU_BUTTONS
from database.database import users_db
from keyboards.keyboards import menu_kb, yes_no_name_kb

from aiogram.fsm.context import FSMContext
from fsm.fsm import FSM_SET_NAME


router = Router()


# Хендлер на кнопку "ДА" заносит пользователя в базу данных и выводит главное меню
@router.callback_query(F.data == 'of_course')
async def of_course_answer(callback: CallbackQuery):
    users_db[callback.from_user.id] = {'name': callback.from_user.full_name}
    await callback.message.edit_text(text='Отлично)\n\n')
    await callback.message.answer(text=f'{LEXICON_MENU_BUTTONS["text_menu"]}', reply_markup=menu_kb())


# Хендлер на кнопку "Изменить имя" устанавливает машину состояний: ожидание ввода имени +
# Хендлер на кнопку "НЕТ" - даем пользователю возможность ввести имя еще раз
@router.callback_query(F.data == 'another name')
@router.callback_query(F.data == 'not', StateFilter(FSM_SET_NAME.enter_name))
async def replace_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_SET_USER_NAME['what_is_your_name'])
    await callback.answer()
    await state.set_state(FSM_SET_NAME.enter_name)


# Хендлер на введенное имя, записывает введенное имя в хранилище, спрашивает: оставить имя или нет?
@router.message(StateFilter(FSM_SET_NAME.enter_name))
async def name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=f'Оставим имя "{message.text}" ?', reply_markup=yes_no_name_kb())


# Хендлер на кнопку ДА (подтверддение имени) - заносит имя в базу, приветствует, предлагает меню
@router.callback_query(F.data == 'confirm', StateFilter(FSM_SET_NAME.enter_name))
async def confirm(callback: CallbackQuery, state: FSMContext):
    # заносим имя в базу из хранилища
    users_db[callback.from_user.id] = await state.get_data()
    await state.clear()
    await callback.message.answer(
        text=f'Приветствую тебя, {users_db[callback.from_user.id]["name"]}!\n\n'
             f'{LEXICON_MENU_BUTTONS["text_menu"]}',
             reply_markup=menu_kb()
    )
