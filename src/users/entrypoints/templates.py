from aiogram import html

from src.users.domain.models import UserModel


class TemplateCreator:

    @staticmethod
    async def start_message(user: UserModel) -> str:
        return f'Hello, {html.bold(user.first_name)}!'
