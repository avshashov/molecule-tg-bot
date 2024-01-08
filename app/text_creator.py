from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import PictureStatus
from app.database.crud import CRUDUser


# формирование сообшений
class TextCreator:
    @staticmethod
    async def create_text_ready(
        session: AsyncSession, user_id: int, mode: str, **kwargs
    ) -> str:
        text = ''
        if mode == PictureStatus.READY:
            full_name, username = await TextCreator._get_username_and_full_name(
                session, user_id
            )
            text += (
                f'Заказ: Готовая картина\n\n'
                f'Имя: {full_name}'
                f'\nКонтакт: @{username}\n'
            )
            if 'enter_telephone' in kwargs:
                text += (
                    f'Телефон: {kwargs.get("enter_telephone", "-")}\n'
                    f'Способ связи: {kwargs.get("how_contact", "-")}\n'
                )
            elif 'enter_email' in kwargs:
                text += f'Email: {kwargs.get("enter_email", "-")}\n'
        return text

    @staticmethod
    async def create_text_order(
        session: AsyncSession, user_id: int, mode: str, **kwargs
    ) -> str:
        text = ''
        if mode == PictureStatus.ORDER:
            full_name, username = await TextCreator._get_username_and_full_name(
                session, user_id
            )
            text += f'Заказ картины\n\n' f'Имя: {full_name}\nКонтакт: @{username}\n'
            if 'enter_telephone' in kwargs:
                text += (
                    f'Телефон: {kwargs.get("enter_telephone", "-")}\n'
                    f'Способ связи: {kwargs.get("how_contact", "-")}\n'
                )
            elif 'enter_email' in kwargs:
                text += f'Email: {kwargs.get("enter_email", "-")}\n'
            text += (
                f'Кому картина: {kwargs.get("for_whom", "   ---")}\n'
                f'Событие: {kwargs.get("event", "   ---")}\n'
                f'Размер: {kwargs.get("size", "   ---")}\n'
                f'Настроение: {kwargs.get("mood", "   ---")}\n'
                f'Цвета: {kwargs.get("color", "   ---")}'
            )
        return text

    @staticmethod
    async def create_text_rent(
        session: AsyncSession, user_id: int, mode: str, **kwargs
    ) -> str:
        text = ''
        if mode == PictureStatus.RENT:
            full_name, username = await TextCreator._get_username_and_full_name(
                session, user_id
            )
            text += (
                f'Заказ: Аренда помещения\n\n'
                f'Имя: {full_name}\n'
                f'Контакт: @{username}\n'
                f'Телефон: {kwargs["enter_telephone"]}\n'
                f'Способ связи: {kwargs["how_contact"]}\n'
                f'Дата: {kwargs["date"]}\n'
                f'Мероприятие: {kwargs["event"]}\n'
                f'Сколько человек: {kwargs["how_people"]}\n'
            )
        return text

    @staticmethod
    async def _get_username_and_full_name(
        session: AsyncSession, user_id: int
    ) -> tuple[str, str] | None:
        """
        Метод получения никнейма и полного имени пользователя по telegram user ID.

        :param session: Асинхронная сессия.
        :param user_id: Телеграм ID.
        :return: Кортеж из никнейма и имени.
        """
        user = await CRUDUser.get_user(session, user_id)
        if user:
            return user.full_name, user.username
