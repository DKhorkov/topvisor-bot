import pytest
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

from src.tasks.entrypoints.schemas import UserActiveTaskScheme
from src.tasks.constants import CallbackDataActions, MarkupButtons, CallbackDataPrefixes
from src.tasks.entrypoints.markups import MarkupCreator
from tests.config import FakeTaskConfig, FakeTaskAssociationConfig


@pytest.mark.anyio
async def test_markup_creator_complete_task_markup_with_tasks() -> None:
    tasks: List[UserActiveTaskScheme] = [
        UserActiveTaskScheme(task_association_id=FakeTaskAssociationConfig.ID, description=FakeTaskConfig.DESCRIPTION)
    ]

    complete_task_markup: InlineKeyboardMarkup = await MarkupCreator.complete_task_markup(tasks=tasks)
    assert len(complete_task_markup.inline_keyboard) == 1

    button: InlineKeyboardButton = complete_task_markup.inline_keyboard[0][0]
    assert button.text == FakeTaskConfig.DESCRIPTION
    assert button.callback_data == (
        f'{CallbackDataPrefixes.COMPLETE_TASK}:'
        f'{CallbackDataActions.COMPLETE_TASK.value}:'
        f'{FakeTaskAssociationConfig.ID}'
    )


@pytest.mark.anyio
async def test_markup_creator_complete_task_markup_without_tasks() -> None:
    complete_task_markup: InlineKeyboardMarkup = await MarkupCreator.complete_task_markup(tasks=[])
    assert len(complete_task_markup.inline_keyboard) == 0


@pytest.mark.anyio
async def test_markup_creator_confirm_task_completeness_markup() -> None:
    confirm_task_completeness_markup: InlineKeyboardMarkup = await MarkupCreator.confirm_task_completeness_markup(
        task_association_id=FakeTaskAssociationConfig.ID
    )

    assert len(confirm_task_completeness_markup.inline_keyboard) == 1

    button: InlineKeyboardButton = confirm_task_completeness_markup.inline_keyboard[0][0]
    assert button.text == MarkupButtons.CONFIRM_TASK_COMPLETENESS
    assert button.callback_data == (
        f'{CallbackDataPrefixes.CONFIRM_TASK_COMPLETENESS}:'
        f'{CallbackDataActions.CONFIRM_TASK_COMPLETENESS.value}:'
        f'{FakeTaskAssociationConfig.ID}'
    )
