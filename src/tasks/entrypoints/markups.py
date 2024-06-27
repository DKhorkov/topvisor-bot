from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from src.tasks.constants import MARKUP_MAX_LENGTH
from src.tasks.entrypoints.callback_data import CompleteTaskCallbackData, CallbackActions
from src.tasks.entrypoints.schemas import UserActiveTaskScheme


class MarkupCreator:

    @staticmethod
    async def complete_task_markup(tasks: List[UserActiveTaskScheme]) -> InlineKeyboardMarkup:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.max_width = MARKUP_MAX_LENGTH
        for task in tasks:
            builder.button(
                text=task.description,
                callback_data=CompleteTaskCallbackData(
                    task_association_id=task.task_association_id,
                    action=CallbackActions.complete_task
                )
            )

        return builder.as_markup()
