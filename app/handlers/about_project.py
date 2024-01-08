from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import MediaBlock, MediaType
from app.database.crud import CRUDMedia
from app.keyboards.about_project_kb import about_project
from app.lexicon.lexicon_ru import LEXICON_ABOUT_PROJECT, LEXICON_MENU_BUTTONS

router = Router()


# Хендлер на кнопку меню 'О проекте'
@router.message(F.text == LEXICON_MENU_BUTTONS['project'])
async def projects_button(message: Message):
    await message.answer(
        text=LEXICON_ABOUT_PROJECT['about_project'], reply_markup=about_project()
    )


# Хендлер на кнопку 'Скачать PDF презентацию'
@router.callback_query(F.data == 'download_presentation')
async def download_presentation(callback: CallbackQuery, session: AsyncSession):
    media = await CRUDMedia.get_media(
        session,
        media_type_id=MediaType.PRESENTATION,
        media_block_id=MediaBlock.ABOUT_PROJECT,
    )
    await callback.message.delete()
    if media:
        presentation = media[-1]
        await callback.message.answer_document(
            document=presentation.media_id,
            reply_markup=about_project(),
        )
    else:
        await callback.message.answer(
            text='Извини, презентация пока не готова', reply_markup=about_project()
        )