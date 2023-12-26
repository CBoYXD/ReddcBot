from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, InlineQuery, Message

from ..config import get_config


class AdminFilter(BaseFilter):
    admin_ids = get_config().admin_ids

    async def __call__(self, obj: InlineQuery | CallbackQuery | Message) -> bool:
        return (obj.from_user.id in self.admin_ids) is True


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_types: list):
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types
