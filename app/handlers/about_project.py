from aiogram import Bot
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_ABOUT_PROJECT, LEXICON_MENU_BUTTONS
from app.database.database import preza
from app.keyboards.about_project_kb import about_project


router = Router()


# Хендлер на кнопку меню 'О проекте'
@router.message(F.text == LEXICON_MENU_BUTTONS['project'])
async def projects_button(message: Message):
    await message.answer(text=LEXICON_ABOUT_PROJECT['about_project'], reply_markup=about_project())


# Хендлер чтобы поймать ID файла презентации
# @router.message(F.document)
# async def document(message: Message):
#    print(message.model_dump_json())
#    presentation_id['file_name'] = message.document.file_name
#    presentation_id['file_id'] = message.document.file_id
#    presentation_id['file_unique_id'] = message.document.file_unique_id
#    print(presentation_id)


# Хендлер на кнопку 'Скачать PDF презентацию'
@router.callback_query(F.data == 'download_presentation')
async def download_presentation(callback: CallbackQuery, bot: Bot):
    if 'file_id' in preza:
        await bot.send_document(chat_id=callback.from_user.id, document=preza['file_id'])
    else:
        await callback.message.answer(text='Извини, презентация пока не готова')
    await callback.answer()
