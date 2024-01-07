from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import BlockText
from app.database.crud import CRUDBlockText
from app.fsm.fsm import FSMAdminContacts
from app.keyboards.admin.common_kb import cancel_kb
from app.keyboards.admin.contacts import contacts_menu_kb
from app.schemas import BlockTextCreate

router = Router()


@router.callback_query(F.data == 'admin contacts command')
async def admin_contacts_menu(callback: CallbackQuery, session: AsyncSession):
    contacts = await CRUDBlockText.get_text_by_block(session, block=BlockText.CONTACTS)
    if contacts:
        text = f'Текущие контакты /contacts:\n\n{contacts}'
    else:
        text = f'Контакты не заданы'
    await callback.message.edit_text(
        text=text,
        reply_markup=contacts_menu_kb(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data == 'add edit contacts')
async def admin_contacts_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text='Введи текст, который будет использоваться при нажатии на команду /contacts - Контакты',
        reply_markup=cancel_kb(),
    )
    await state.set_state(FSMAdminContacts.enter_contacts)


@router.message(~(F.text == 'Отмена'), StateFilter(FSMAdminContacts.enter_contacts))
async def get_contacts(message: Message, state: FSMContext, session: AsyncSession):
    text = message.md_text.strip()
    if await CRUDBlockText.get_text_by_block(session, block=BlockText.CONTACTS):
        text = await CRUDBlockText.update_text_by_block(
            session, block=BlockText.CONTACTS, text=text
        )
    else:
        await CRUDBlockText.create_block_text(
            session, text_fields=BlockTextCreate(text=text, block=BlockText.CONTACTS)
        )
    await message.answer(text='Контакты добавлены', reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text=f'Текущие контакты /contacts:\n\n{text}',
        reply_markup=contacts_menu_kb(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await state.clear()


@router.message(
    F.text == 'Отмена',
    StateFilter(FSMAdminContacts.enter_contacts),
)
async def cancel_add_contacts(
    message: Message, state: FSMContext, session: AsyncSession
):
    contacts = await CRUDBlockText.get_text_by_block(session, block=BlockText.CONTACTS)
    if contacts:
        text = f'Текущие контакты /contacts:\n\n{contacts}'
    else:
        text = f'Контакты не заданы'
    await message.answer(text='Действие отменено', reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text=text,
        reply_markup=contacts_menu_kb(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await state.clear()
