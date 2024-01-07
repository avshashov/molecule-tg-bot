from sqlalchemy import delete, select, update, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database.models import Picture


class CRUDPicture:
    @staticmethod
    async def create_picture(
        session: AsyncSession, picture_fields: schemas.PictureCreate
    ) -> None:
        """
        Метод создания картины в таблице Picture.

        :param session: Асинхронная сессия.
        :param picture_fields: Данные картины.
        """
        picture = Picture(**picture_fields.model_dump())
        session.add(picture)
        await session.commit()

    @staticmethod
    async def get_pictures(session: AsyncSession) -> list[Picture]:
        """
        Метод получения списка картин

        :param session: Асинхронная сессия.
        :return: Список картин.
        """
        query = select(Picture).order_by(asc(Picture.created_at))
        stmt = await session.execute(query)
        return list(stmt.scalars())

    @staticmethod
    async def get_picture_by_id(session: AsyncSession, id: int) -> Picture:
        """
        Метод получения картины по ID.

        :param session: Асинхронная сессия.
        :param id: Первичный ключ картины в БД.
        :return: Сущность картины.
        """

        query = select(Picture).where(Picture.id == id)
        stmt = await session.execute(query)
        return stmt.scalar()

    @staticmethod
    async def delete_picture(session: AsyncSession, id: int) -> None:
        """
        Метод удаление картины по телеграм picture_id.

        :param session: Асинхронная сессия.
        :param id: Первичный ключ картины в БД.
        """
        query = delete(Picture).where(Picture.id == id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def update_picture(
        session: AsyncSession, id: int, picture_fields: schemas.PictureUpdate
    ) -> Picture:
        """
        Метод обновления картины по ID.

        :param session: Асинхронная сессия.
        :param id: Первичный ключ картины в БД.
        :param picture_fields: Новые значения для картины.
        :return: Обновленная картина.
        """
        query = (
            update(Picture)
            .where(Picture.id == id)
            .values(**picture_fields.model_dump(exclude_none=True))
            .returning(Picture)
        )
        stmt = await session.execute(query)
        await session.commit()
        return stmt.scalar()
