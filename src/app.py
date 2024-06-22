from aiogram import Dispatcher

from src.help.entrypoints.router import help_router
from src.users.entrypoints.router import users_router
from src.clean.entrypoints.router import clean_router


dispatcher: Dispatcher = Dispatcher()
dispatcher.include_router(users_router)
dispatcher.include_router(help_router)
dispatcher.include_router(clean_router)  # Should be last included router not to delete valid messages
