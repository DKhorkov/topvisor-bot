from aiogram.filters.callback_data import CallbackData

from src.tasks.constants import CallbackDataActions, CallbackDataPrefixes

"""
All data length, stored in CallbackData classes, must not exceed 64 chars, including standard separators and prefix.
"""


class CompleteTaskCallbackData(CallbackData, prefix=CallbackDataPrefixes.COMPLETE_TASK):
    action: CallbackDataActions
    task_association_id: int


class ConfirmTaskCompletenessCallbackData(CallbackData, prefix=CallbackDataPrefixes.CONFIRM_TASK_COMPLETENESS):
    action: CallbackDataActions
    task_association_id: int
