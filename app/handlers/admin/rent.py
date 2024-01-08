from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import MediaBlock, MediaType, BlockText
from app.database.crud import CRUDMedia, CRUDBlockText
from app.fsm.fsm import FSMAdminRent
from app.keyboards.admin.rent_kb import (
    cancel_send_rent_photo_kb,
    confirm_delete_rent_photo_kb,
    edit_rent_photo_kb,
    list_of_current_rent_photo_kb,
    open_rent_photo_kb,
    rent_menu_kb,
    cancel_change_rent_photo_title,
    cancel_change_rent_text,
)
from app.schemas import BlockTextCreate, MediaCreate, MediaUpdate

router = Router()


@router.callback_query(F.data == 'admin rent')
async def admin_rent_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Настройка блока аренды', reply_markup=rent_menu_kb()
    )


@router.callback_query(F.data == 'edit rent photo')
async def edit_rent_photo_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'Здесь ты можешь загрузить новое фото или изменить/удалить текущие',
        reply_markup=edit_rent_photo_kb(),
    )


@router.callback_query(F.data == 'add new rent photo')
async def add_new_rent_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f'Загрузи новое фото как обычную картинку (не документ)',
        reply_markup=cancel_send_rent_photo_kb(),
    )
    await state.set_state(FSMAdminRent.send_rent_photo)


@router.message(F.photo, StateFilter(FSMAdminRent.send_rent_photo))
async def send_photo(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[2].file_id)
    await message.answer(
        text='Введи короткое название к фотографии, '
        'это название будет использоваться в блоке редактирования фотографий.'
        '\nПользователь этого названия не увидит.'
        '\n\nНапример: Основной ракурс',
        reply_markup=cancel_send_rent_photo_kb(),
    )
    await state.set_state(FSMAdminRent.enter_photo_title)


@router.message(F.text, StateFilter(FSMAdminRent.enter_photo_title))
async def get_photo_title(message: Message, state: FSMContext, session: AsyncSession):
    text = message.text.strip()
    data = await state.get_data()
    media = MediaCreate(
        media_id=data['photo_id'],
        title=text,
        media_type_id=MediaType.PHOTO,
        media_block_id=MediaBlock.RENT,
    )
    await CRUDMedia.create_media(session, media)
    await message.answer(text='Фото добавлено', reply_markup=edit_rent_photo_kb())


@router.callback_query(F.data == 'back rent menu')
async def back_to_rent_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Настройка блока аренды',
        reply_markup=rent_menu_kb(),
    )


@router.callback_query(F.data == 'cancel send rent photo')
async def cancel_send_rent_photo(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Здесь ты можешь загрузить новое фото или изменить/удалить текущие',
        reply_markup=edit_rent_photo_kb(),
    )


@router.callback_query(F.data == 'confirm delete rent photo')
@router.callback_query(F.data == 'back list rent photo')
@router.callback_query(F.data == 'edit current rent photo')
async def confirm_delete_or_edit_current_rent_photo(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    if callback.data == 'confirm delete rent photo':
        data = await state.get_data()
        await CRUDMedia.delete_media(session, id=int(data['photo_id']))
    list_photo = await CRUDMedia.get_media(
        session=session, media_type_id=MediaType.PHOTO, media_block_id=MediaBlock.RENT
    )
    await callback.message.delete()
    await callback.message.answer(
        text='Раздел редактирования текущих фотографий',
        reply_markup=list_of_current_rent_photo_kb(list_photo),
    )
    await state.set_state(FSMAdminRent.open_photo)


@router.callback_query(F.data == 'back edit rent photo')
async def back_to_edit_rent_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text='Здесь ты можешь загрузить новое фото или изменить/удалить текущие',
        reply_markup=edit_rent_photo_kb(),
    )
    await state.clear()


@router.callback_query(F.data == 'delete rent photo')
async def delete_rent_photo_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=confirm_delete_rent_photo_kb()
    )


@router.callback_query(F.data == 'change rent photo title')
async def change_rent_photo_title(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text='Введи новый заголовок',
        reply_markup=cancel_change_rent_photo_title(),
    )
    data = await state.get_data()
    await state.set_state(FSMAdminRent.enter_new_photo_title)
    await state.update_data(**data)


@router.message(F.text, StateFilter(FSMAdminRent.enter_new_photo_title))
async def get_new_photo_title(
    message: Message, state: FSMContext, session: AsyncSession
):
    text = message.text.strip()
    data = await state.get_data()
    photo = await CRUDMedia.update_media(
        session, id=data['photo_id'], media_fields=MediaUpdate(title=text)
    )
    await message.answer_photo(
        photo=photo.media_id, caption=text, reply_markup=open_rent_photo_kb()
    )
    await state.set_state(FSMAdminRent.open_photo)
    await state.update_data(**data)


@router.callback_query(F.data == 'cancel delete rent photo')
async def cancel_delete_rent_photo(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=open_rent_photo_kb())


@router.callback_query(F.data == 'cancel change rent title')
@router.callback_query(StateFilter(FSMAdminRent.open_photo))
async def open_rent_photo(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    if callback.data.startswith('cancel'):
        data = await state.get_data()
        await state.set_state(FSMAdminRent.open_photo)
        await state.update_data(**data)
        photo_id = (await state.get_data()).get('photo_id')
    else:
        photo_id = int(callback.data)
        await state.update_data(photo_id=photo_id)
    await callback.message.delete()
    photo = await CRUDMedia.get_media_by_id(session, id=photo_id)
    text = f'Заголовок: {photo.title}'
    await callback.message.answer_photo(
        photo=photo.media_id, caption=text, reply_markup=open_rent_photo_kb()
    )


@router.callback_query(F.data == 'change rent text')
async def send_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Введи новый текст для блока Аренда',
        reply_markup=cancel_change_rent_text(),
    )
    await state.set_state(FSMAdminRent.enter_new_rent_text)


@router.message(F.text, StateFilter(FSMAdminRent.enter_new_rent_text))
async def get_new_rent_text(message: Message, state: FSMContext, session: AsyncSession):
    text = message.md_text.strip()
    if await CRUDBlockText.get_text_by_block(session, block=BlockText.RENT):
        await CRUDBlockText.update_text_by_block(
            session, block=BlockText.RENT, text=text
        )
    else:
        await CRUDBlockText.create_block_text(
            session, text_fields=BlockTextCreate(text=text, block=BlockText.RENT)
        )
    await message.answer(text='Текст изменен')
    await message.answer(text='Настройка блока аренды', reply_markup=rent_menu_kb())
    await state.clear()


@router.callback_query(F.data == 'view rent block')
async def view_rent_block(callback: CallbackQuery, session: AsyncSession):
    text = await CRUDBlockText.get_text_by_block(session, block=BlockText.RENT)
    if text:
        await callback.message.edit_text(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        photos = await CRUDMedia.get_media(
            session, media_type_id=MediaType.PHOTO, media_block_id=MediaBlock.RENT
        )
        if photos:
            photos = [InputMediaPhoto(media=photo.media_id) for photo in photos]
            if photos:
                await callback.message.answer_media_group(media=photos)
        await callback.message.answer(
            text='Настройка блока аренды', reply_markup=rent_menu_kb()
        )
    else:
        await callback.message.delete()
        await callback.message.answer(
            text='Описание отсутствует.' '\n\nНастройка блока аренды',
            reply_markup=rent_menu_kb(),
        )
