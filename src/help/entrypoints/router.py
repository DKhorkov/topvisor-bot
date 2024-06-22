from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.constants import CommandNames


help_router: Router = Router()


@help_router.message(Command(CommandNames.HELP))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """

    await message.delete()
    await message.answer('some help info')
