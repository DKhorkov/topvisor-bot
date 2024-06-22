from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.users.domain.models import UserModel
from src.users.entrypoints.dependencies import register_user


users_router: Router = Router()


@users_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    await message.delete()
    user: UserModel = await register_user(message=message)
    await message.answer(f"Hello, {html.bold(user.first_name)}!")