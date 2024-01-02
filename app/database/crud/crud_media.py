from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database.models import Media, MediaBlock, MediaType


class CRUDMedia:
    @staticmethod
    async def create_media(
        session: AsyncSession, media_fields: schemas.MediaCreate
    ) -> None:
        """
        Метод создания медиа в таблице Media.

        :param session: Асинхронная сессия.
        :param media_fields: Данные медиа.
        """
        media = Media(**media_fields.model_dump())
        session.add(media)
        await session.commit()

    @staticmethod
    async def get_media(
        session: AsyncSession, media_type_id: int, media_block_id: int
    ) -> list[Media]:
        """
        Метод получения медиафайлов с фильтрацией по типу и блоку медиа

        :param session: Асинхронная сессия.
        :param media_type_id: ID типа медиа.
        :param media_block_id: ID блока медиа.
        :return: Список медиа.
        """
        query = (
            select(Media)
            .join(MediaType)
            .join(MediaBlock)
            .where(MediaType.id == media_type_id, MediaBlock.id == media_block_id)
        )
        stmt = await session.execute(query)
        return list(stmt.scalars())

    @staticmethod
    async def delete_media(session: AsyncSession, media_id: int) -> None:
        """
        Метод удаление медиафайла по телеграм медиа ID

        :param session: Асинхронная сессия.
        :param media_id: Телеграм медиа ID.
        """
        query = delete(Media).where(Media.id == media_id)
        await session.execute(query)

    @staticmethod
    async def update_media(
        session: AsyncSession, media_id: int, media_fields: schemas.MediaUpdate
    ) -> Media:
        """
        Метод обновления медиафайла по телеграм медиа ID

        :param session: Асинхронная сессия.
        :param media_id: Телеграм медиа ID.
        :param media_fields: Новые значения для медиа.
        :return: Обновленное медиа.
        """
        query = (
            update(Media)
            .where(Media.media_id == media_id)
            .values(**media_fields.model_dump(exclude_none=True))
            .returning(Media)
        )
        stmt = await session.execute(query)
        return stmt.scalar()
