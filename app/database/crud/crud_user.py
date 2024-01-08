from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database.models import User


class CRUDUser:
    @staticmethod
    async def create_user(
        session: AsyncSession, user_fields: schemas.UserCreate
    ) -> None:
        """
        Метод создания пользователя в таблице User.

        :param session: Асинхронная сессия.
        :param user_fields: Данные пользователя.
        """
        user = User(**user_fields.model_dump())
        session.add(user)
        await session.commit()

    @staticmethod
    async def get_user(session: AsyncSession, tg_user_id: int) -> User | None:
        """
        Метод получения пользователя по его телеграм ID.

        :param session: Асинхронная сессия.
        :param tg_user_id: Телеграм ID.
        :return: Сущность пользователя.
        """
        query = select(User).where(User.user_id == tg_user_id)
        stmt = await session.execute(query)
        return stmt.scalar()

    @staticmethod
    async def get_tg_user_ids(session: AsyncSession) -> list[int]:
        """
        Метод получения телеграм ID пользователей.

        :param session: Асинхронная сессия.
        :return: Список телеграм id пользователей.
        """
        stmt = await session.execute(select(User.user_id))
        return list(stmt.scalars())

    @staticmethod
    async def user_exists(session: AsyncSession, tg_user_id: int) -> bool:
        """
        Метод проверки наличия пользователя в таблице User.

        :param session: Асинхронная сессия.
        :param tg_user_id: Телеграм ID.
        :return: True/False
        """
        query = select(User).where(User.id == tg_user_id)
        stmt = await session.execute(query)
        return bool(stmt)
    
    @staticmethod
    async def get_user_full_name(session: AsyncSession, tg_user_id: int) -> str | None:
        """
        Метод получения имени пользователя.

        :param session: Асинхронная сессия.
        :param tg_user_id: Телеграм ID.
        :return: Сущность пользователя.
        """
        query = select(User.full_name).where(User.user_id == tg_user_id)
        stmt = await session.execute(query)
        return stmt.scalar()
