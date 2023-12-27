from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from ...filters import AdminFilter
from ...misc.states import AdminState

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("start"))
async def admin_msg_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminState.posts.choose, mode=StartMode.RESET_STACK)
