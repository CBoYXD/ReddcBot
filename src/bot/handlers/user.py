from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

user_router = Router()


@user_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Вітаю, адміне!")
