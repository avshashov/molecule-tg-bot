import asyncio
import logging
import random

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.crud import CRUDPicture, CRUDUser
from app.database.models import Picture

logger = logging.getLogger(__name__)


async def send_random_picture(session_maker: async_sessionmaker, bot: Bot) -> None:
    """
    Метод отправки случайной картины всем пользователям.

    :param session_maker: Асинхронная фабрика сессий.
    :param bot: Экземляр телеграм бота.
    """
    async with session_maker() as session:
        media = await CRUDPicture.get_pictures(session)
        user_ids = await CRUDUser.get_tg_user_ids(session)

    if not media:
        return

    picture: Picture = random.choice(media)
    for user_id in user_ids:
        logger.info('[SCHEDULER] Рассылка начата.')
        try:
            await bot.send_photo(
                chat_id=user_id, photo=picture.picture_id, caption=picture.description
            )
            await asyncio.sleep(0.05)
        except TelegramForbiddenError:
            continue
    logger.info('[SCHEDULER] Рассылка завершена.')
