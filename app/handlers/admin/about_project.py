from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import MediaBlock, MediaType
from app.database.crud import CRUDMedia
from app.fsm.fsm import FSMAdminAboutProject
from app.keyboards.admin.about_project_kb import (
    admin_about_project_menu_kb,
    cancel_upload_presentation,
)
from app.keyboards.admin.common_kb import admin_panel_kb
from app.schemas import MediaCreate

router = Router()


@router.callback_query(F.data == 'cancel upload presentation')
@router.callback_query(F.data == 'admin about project')
async def admin_about_project_menu(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await state.clear()
    media = await CRUDMedia.get_media(
        session,
        media_type_id=MediaType.PRESENTATION,
        media_block_id=MediaBlock.ABOUT_PROJECT,
    )
    if media:
        presentation = media[-1]
        await callback.message.delete()
        await callback.message.answer_document(
            document=presentation.media_id,
            caption='Текущая презентация',
            reply_markup=admin_about_project_menu_kb(),
        )
    else:
        await callback.message.edit_text(
            text='Презентация не загружена', reply_markup=admin_about_project_menu_kb()
        )


@router.callback_query(F.data == 'add change presentation')
async def add_presentation_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text='Загрузи презентацию', reply_markup=cancel_upload_presentation()
    )
    await state.set_state(FSMAdminAboutProject.upload_presentation)


@router.callback_query(F.data == 'back admin panel from project')
async def back_to_admin_panel(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=f'Панель администратора.'
        f'\n\nДля изменения наполнения конкретного раздела выбери кнопку ниже:',
        reply_markup=admin_panel_kb(),
    )


@router.message(F.document, StateFilter(FSMAdminAboutProject.upload_presentation))
async def get_presentation(message: Message, state: FSMContext, session: AsyncSession):
    file_id = message.document.file_id
    media = MediaCreate(
        title=message.document.file_name,
        media_id=file_id,
        media_type_id=MediaType.PRESENTATION,
        media_block_id=MediaBlock.ABOUT_PROJECT,
    )
    await CRUDMedia.create_media(session, media_fields=media)
    await message.answer_document(
        document=file_id,
        caption='Текущая презентация',
        reply_markup=admin_about_project_menu_kb(),
    )
    await state.clear()
