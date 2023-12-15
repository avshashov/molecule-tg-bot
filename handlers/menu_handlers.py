from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from database.database import users_db
from keyboards.keyboards import yes_no_kb, menu_kb
from lexicon.lexicon_ru import LEXICON_SET_USER_NAME, LEXICON_MENU_BUTTONS

from aiogram.fsm.context import FSMContext
from fsm.fsm import FSM_SET_NAME


router = Router()


# Хендлер на команду "/start" - будет
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    if message.from_user.id in users_db:  # Если пользователь уже в базе
        await message.answer(
            text=f'Приветствую тебя, {users_db[message.from_user.id]["name"]}, я Небула - бот Молекулы\n\n'
            f'{LEXICON_MENU_BUTTONS["text_menu"]}',
            reply_markup=menu_kb()
        )

    elif message.from_user.full_name:  # Если указан фулл нейм
        await message.answer(
            text=f'Приветствую тебя, {message.from_user.full_name}, я Небула - бот Молекулы\n\n'
            'Могу ли я к тебе так обращаться?',
            reply_markup=yes_no_kb()
        )
        # если да то заносим имя в базу
        # если нет то устанавливаем машину состояний: ожидание ввода имени,
        # пользователь указывает имя, далее заносим его в базу

    else:  # Если пользователя нет в базе и не указан фулл нейм
        await message.answer(text=LEXICON_SET_USER_NAME['unknown'])
        # устанавливаем машину состояний: ожидание ввода имени, пользователь указывает имя, заносим в базу
        await state.set_state(FSM_SET_NAME.enter_name)


# Хендлер на команду "/contacts"
@router.message(Command(commands='contacts'))
async def contacts_command(message: Message):
    await message.answer(text=LEXICON_MENU_BUTTONS['contacts'])


# Хендлер на команду "/invite"
@router.message(Command(commands='invite'))
async def invite_command(message: Message):
    await message.answer(text=f'{LEXICON_MENU_BUTTONS["invite"]}\n\nhttps://t.me/Molecule_nebula_bot')


# Хендлер на кнопку 'Главное меню'
@router.callback_query(F.data == 'main_menu')
async def main_menu_button(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_MENU_BUTTONS["text_menu"], reply_markup=menu_kb())
    await callback.answer()
