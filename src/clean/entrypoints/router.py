from aiogram import Router
from aiogram.types import Message

clean_router: Router = Router()


@clean_router.message()
async def trash_messages_handler(message: Message) -> None:
    """
    Handler will receive any message from user, which should not be handled by other routers and handlers,
    and deletes received message.
    """

    await message.delete()
