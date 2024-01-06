from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class MessageAdminFilter(BaseFilter):
    def __init__(self, admin_chat_id: int) -> None:
        self.admin_chat_id = admin_chat_id

    async def __call__(self, message: Message) -> bool:
        return message.chat.id == self.admin_chat_id


class CallbackAdminFilter(MessageAdminFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.message.chat.id == self.admin_chat_id
