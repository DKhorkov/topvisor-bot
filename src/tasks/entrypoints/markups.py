from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from src.tasks.constants import MARKUP_MAX_LENGTH, CallbackDataActions, MarkupButtons
from src.tasks.entrypoints.callback_data import CompleteTaskCallbackData, ConfirmTaskCompletenessCallbackData
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
                    action=CallbackDataActions.COMPLETE_TASK
                )
            )

        return builder.as_markup()

    @staticmethod
    async def confirm_task_completeness_markup(task_association_id: int) -> InlineKeyboardMarkup:
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.max_width = MARKUP_MAX_LENGTH
        builder.button(
            text=MarkupButtons.CONFIRM_TASK_COMPLETENESS,
            callback_data=ConfirmTaskCompletenessCallbackData(
                action=CallbackDataActions.CONFIRM_TASK_COMPLETENESS,
                task_association_id=task_association_id
            )
        )

        builder.button(
            text=MarkupButtons.REJECT_TASK_COMPLETENESS,
            callback_data=ConfirmTaskCompletenessCallbackData(
                action=CallbackDataActions.REJECT_TASK_COMPLETENESS,
                task_association_id=task_association_id
            )
        )

        return builder.as_markup()
