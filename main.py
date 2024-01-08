import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.settings import bot_db
from app.handlers import about_project, menu_handlers, pictures, rent, set_user_name
from app.handlers.admin import common as admin
from app.jobs import send_random_picture
from app.lexicon.lexicon_ru import LEXICON_SET_MENU
from app.middlewares import SessionMiddleware
from config import config

logger = logging.getLogger(__name__)


async def set_menu_commands(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_SET_MENU.items()
    ]
    await bot.set_my_commands(main_menu_commands)

    main_menu_commands.append(
        BotCommand(command='admin', description='Панель администратора')
    )
    await bot.set_my_commands(
        main_menu_commands,
        scope=BotCommandScopeChat(chat_id=config.tg_bot.admin_group_id),
    )


def setup_dispatcher() -> Dispatcher:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.update.middleware(SessionMiddleware(bot_db.async_session_maker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.include_routers(
        menu_handlers.router,
        set_user_name.router,
        about_project.router,
        rent.router,
        pictures.router,
        admin.router,
    )
    return dp


def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO, format='[%(asctime)s] - %(levelname)s - %(message)s'
    )
    logger.info('Starting bot')


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=send_random_picture,
        trigger=config.scheduler.trigger,
        day=config.scheduler.day,
        hour=config.scheduler.hour,
        minute=config.scheduler.minute,
        args=(bot_db.async_session_maker, bot),
    )
    return scheduler


async def main():
    setup_logger()
    bot = Bot(token=config.tg_bot.token, parse_mode=None)
    dp = setup_dispatcher()
    await set_menu_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler = setup_scheduler(bot)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
