from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import config
from app.filters import CallbackAdminFilter, MessageAdminFilter
from app.handlers.admin.about_project import router as about_project_router
from app.handlers.admin.rent import router as rent_router
from app.handlers.admin.scheduler_settings import router as scheduler_router
from app.keyboards.admin.common_kb import admin_panel_kb

router = Router()
router.include_routers(rent_router, about_project_router, scheduler_router)
router.message.filter(MessageAdminFilter(admin_chat_id=config.tg_bot.admin_group_id))
router.callback_query.filter(
    CallbackAdminFilter(admin_chat_id=config.tg_bot.admin_group_id)
)


@router.message(Command(commands='admin'))
async def admin_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f'Панель администратора.'
        f'\n\nДля изменения наполнения конкретного раздела выбери кнопку ниже:',
        reply_markup=admin_panel_kb(),
    )
