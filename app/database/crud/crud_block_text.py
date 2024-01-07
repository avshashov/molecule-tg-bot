from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database.models import BlockText


class CRUDBlockText:
    @staticmethod
    async def create_block_text(
        session: AsyncSession, text_fields: schemas.BlockTextCreate
    ) -> None:
        """
        Метод создания текста.

        :param session: Асинхронная сессия.
        :param text_fields: Поля текста.
        """
        text = BlockText(**text_fields.model_dump())
        session.add(text)
        await session.commit()

    @staticmethod
    async def get_text_by_block(session: AsyncSession, block: str) -> str | None:
        """
        Метод получения текста по названию блока.

        :param session: Асинхронная сессия.
        :param block: Название блока.
        :return: Текст блока.
        """
        query = select(BlockText.text).where(BlockText.block == block)
        stmt = await session.execute(query)
        return stmt.scalar()

    @staticmethod
    async def update_text_by_block(session: AsyncSession, block: str, text: str) -> str:
        """
        Метод обновления текста по названию блока.

        :param session: Асинхронная сессия.
        :param block: Название блока.
        :param text: Новый текст блока.
        :return: Текст блока.
        """
        query = (
            update(BlockText)
            .where(BlockText.block == block)
            .values(text=text)
            .returning(BlockText.text)
        )
        stmt = await session.execute(query)
        await session.commit()
        return stmt.scalar()
