from aiogram.filters.callback_data import CallbackData

from src.tasks.constants import CallbackDataActions

"""
All data length, stored in CallbackData classes, must not exceed 64 chars, including standard separators.
"""


class CompleteTaskCallbackData(CallbackData, prefix='complete_task'):
    action: CallbackDataActions
    task_association_id: int


class ConfirmTaskCompletenessCallbackData(CallbackData, prefix='confirm_task_completeness'):
    action: CallbackDataActions
    task_association_id: int
