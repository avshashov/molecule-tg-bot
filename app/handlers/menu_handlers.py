from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import BlockText
from app.database.crud import CRUDBlockText, CRUDUser
from app.fsm.fsm import FSM_SET_NAME
from app.keyboards.menu_kb import menu_kb
from app.keyboards.user_name_setting import yes_no_kb
from app.lexicon.lexicon_ru import LEXICON_MENU_BUTTONS, LEXICON_SET_USER_NAME

router = Router()


# Хендлер на команду "/start" - будет
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    if full_name := await CRUDUser.get_user_full_name(session, message.from_user.id):
        await message.answer(
            text=f'Приветствую тебя 🤝, {full_name}, я Небула🌀 - бот Молекулы©️',
            reply_markup=menu_kb(),
        )

    elif message.from_user.full_name:  # Если указан фулл нейм
        await message.answer(
            text=f'Приветствую тебя 🤝, {message.from_user.full_name}, я Небула🌀 - бот Молекулы©️\n\n'
            'Могу ли я к тебе так обращаться?',
            reply_markup=yes_no_kb(),
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
async def contacts_command(message: Message, session: AsyncSession):
    contacts = await CRUDBlockText.get_text_by_block(session, block=BlockText.CONTACTS)
    text = contacts if contacts else 'Контакты не заданы'
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


# Хендлер на команду "/invite"
@router.message(Command(commands='invite'))
async def invite_command(message: Message):
    bot = await message.bot.get_me()
    await message.answer(
        text=f'{LEXICON_MENU_BUTTONS["invite"]}\n\nhttps://t.me/{bot.username}'
    )


# Хендлер на кнопку 'Главное меню'
@router.callback_query(F.data == 'main_menu')
async def main_menu_button(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON_MENU_BUTTONS["text_menu"], reply_markup=menu_kb()
    )
