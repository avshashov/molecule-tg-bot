from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import users_db
from app.fsm.fsm import FSM_SET_NAME
from app.keyboards.menu_kb import menu_kb
from app.keyboards.user_name_setting import yes_no_name_kb
from app.lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_SET_USER_NAME
from app.database.crud import CRUDUser
from app.schemas import UserCreate


router = Router()


# Хендлер на кнопку "ДА" заносит пользователя в базу данных и выводит главное меню
@router.callback_query(F.data == 'of_course')
async def of_course_answer(callback: CallbackQuery, session: AsyncSession):
    user = UserCreate(
        username=callback.from_user.username, 
        user_id=callback.from_user.id, 
        full_name=callback.from_user.full_name,
        )
    await CRUDUser.create_user(session, user)
    await callback.message.delete()
    await callback.message.answer(text='Отлично 👍\n\n', reply_markup=menu_kb())


# Хендлер на кнопку "Изменить имя" устанавливает машину состояний: ожидание ввода имени +
# Хендлер на кнопку "НЕТ" - даем пользователю возможность ввести имя еще раз
@router.callback_query(F.data == 'another name')
@router.callback_query(F.data == 'not', StateFilter(FSM_SET_NAME.enter_name))
async def replace_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_SET_USER_NAME['what_is_your_name'])
    await state.set_state(FSM_SET_NAME.enter_name)


# Хендлер на введенное имя, записывает введенное имя в хранилище, спрашивает: оставить имя или нет?
@router.message(StateFilter(FSM_SET_NAME.enter_name))
async def name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=f'Оставим имя "{message.text}" ?', reply_markup=yes_no_name_kb()
    )


# Хендлер на кнопку ДА (подтверддение имени) - заносит имя в базу, приветствует, предлагает меню
@router.callback_query(F.data == 'confirm', StateFilter(FSM_SET_NAME.enter_name))
async def confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    # заносим имя в базу из хранилища
    full_name = (await state.get_data()).get('name')
    user = UserCreate(
        username=callback.from_user.username, 
        user_id=callback.from_user.id, 
        full_name=full_name,
        )
    await CRUDUser.create_user(session, user)
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        text=f'Приветствую тебя 🤝, {full_name}!',
        reply_markup=menu_kb(),
    )
