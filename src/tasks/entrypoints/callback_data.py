from enum import Enum
from aiogram.filters.callback_data import CallbackData


class CallbackActions(str, Enum):
    complete_task: str = 'complete_task'


class CompleteTaskCallbackData(CallbackData, prefix='complete_task_callback_data'):
    action: CallbackActions
    task_association_id: int
