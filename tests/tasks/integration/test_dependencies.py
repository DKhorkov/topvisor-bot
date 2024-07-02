import pytest
from typing import List, Optional
from aiogram.types import Message
from sqlalchemy import update, select, CursorResult, Row
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from src.core.database.connection import DATABASE_URL
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.entrypoints.schemas import UserTaskStatisticsResponseScheme, UserActiveTaskScheme
from src.users.domain.models import UserModel
from tests.config import FakeTaskConfig, FakeTaskAssociationConfig, FakeUserConfig
from src.tasks.entrypoints.dependencies import (
    get_user_tasks_statistics,
    get_actual_tasks,
    update_tasks,
    get_user_active_tasks,
    get_task_by_association_id,
    get_user_by_association_id,
    set_task_competed_for_user
)


@pytest.mark.anyio
async def test_get_user_tasks_statistics_with_existing_tasks(create_test_task: None, message: Message) -> None:
    user_tasks_statistics: List[UserTaskStatisticsResponseScheme] = await get_user_tasks_statistics(message=message)
    assert len(user_tasks_statistics) == 1

    task_statistics: UserTaskStatisticsResponseScheme = user_tasks_statistics[0]
    assert task_statistics.description == FakeTaskConfig.DESCRIPTION
    assert task_statistics.is_completed == FakeTaskAssociationConfig.TASK_COMPLETED


@pytest.mark.anyio
async def test_get_user_tasks_statistics_without_existing_tasks(map_models_to_orm: None, message: Message) -> None:
    user_tasks_statistics: List[UserTaskStatisticsResponseScheme] = await get_user_tasks_statistics(message=message)
    assert len(user_tasks_statistics) == 0


@pytest.mark.anyio
async def test_get_actual_tasks_with_existing_actual_tasks(create_test_task: None) -> None:
    tasks: List[TaskModel] = await get_actual_tasks()
    assert len(tasks) == 1

    task: TaskModel = tasks[0]
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_get_actual_tasks_with_existing_archived_tasks(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    await async_connection.execute(
        update(
            TaskModel
        ).filter_by(
            id=FakeTaskConfig.ID
        ).values(
            is_archived=True
        )
    )
    await async_connection.commit()

    tasks: List[TaskModel] = await get_actual_tasks()
    assert len(tasks) == 0


@pytest.mark.anyio
async def test_get_actual_tasks_without_existing_tasks(map_models_to_orm: None) -> None:
    tasks: List[TaskModel] = await get_actual_tasks()
    assert len(tasks) == 0


@pytest.mark.anyio
async def test_get_user_active_tasks_with_existing_actual_tasks(
        create_test_task: None,
        message: Message
) -> None:

    user_active_tasks: List[UserActiveTaskScheme] = await get_user_active_tasks(message=message)
    assert len(user_active_tasks) == 1

    active_task: UserActiveTaskScheme = user_active_tasks[0]
    assert active_task.task_association_id == FakeTaskAssociationConfig.ID
    assert active_task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_get_user_active_tasks_with_existing_archived_tasks(
        create_test_task: None,
        async_connection: AsyncConnection,
        message: Message
) -> None:

    await async_connection.execute(
        update(
            TaskAssociationModel
        ).filter_by(
            id=FakeTaskAssociationConfig.ID
        ).values(
            task_archived=True
        )
    )
    await async_connection.commit()

    user_active_tasks: List[UserActiveTaskScheme] = await get_user_active_tasks(message=message)
    assert len(user_active_tasks) == 0


@pytest.mark.anyio
async def test_get_user_active_tasks_with_existing_completed_tasks(
        create_test_task: None,
        async_connection: AsyncConnection,
        message: Message
) -> None:

    await async_connection.execute(
        update(
            TaskAssociationModel
        ).filter_by(
            id=FakeTaskAssociationConfig.ID
        ).values(
            task_completed=True
        )
    )
    await async_connection.commit()

    user_active_tasks: List[UserActiveTaskScheme] = await get_user_active_tasks(message=message)
    assert len(user_active_tasks) == 0


@pytest.mark.anyio
async def test_get_user_active_tasks_without_existing_tasks(
        map_models_to_orm: None,
        message: Message
) -> None:

    user_active_tasks: List[UserActiveTaskScheme] = await get_user_active_tasks(message=message)
    assert len(user_active_tasks) == 0


@pytest.mark.anyio
async def test_update_tasks_with_no_existing_tasks_and_with_created_user(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskAssociationModel))
    result: Optional[Row] = cursor.first()
    assert result is None

    tasks: List[TaskModel] = [TaskModel(**FakeTaskConfig().to_dict(to_lower=True))]
    await update_tasks(tasks=tasks)

    cursor = await async_connection.execute(select(TaskAssociationModel))
    result = cursor.first()
    assert result is not None
    task_completed: bool = result[3]
    assert not task_completed
    task_archived: bool = result[4]
    assert not task_archived


@pytest.mark.anyio
async def test_update_tasks_with_existing_not_archived_tasks_and_with_created_user(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskAssociationModel))
    result: Optional[Row] = cursor.first()
    assert result is not None

    tasks: List[TaskModel] = [TaskModel(**FakeTaskConfig().to_dict(to_lower=True))]
    updated_tasks: List[TaskModel] = await update_tasks(tasks=tasks)
    assert len(updated_tasks) == 1
    task: TaskModel = updated_tasks[0]
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION
    assert task.is_archived is False

    cursor = await async_connection.execute(select(TaskAssociationModel))
    result = cursor.first()
    assert result is not None
    task_completed: bool = result[3]
    assert not task_completed
    task_archived: bool = result[4]
    assert not task_archived


@pytest.mark.anyio
async def test_update_tasks_with_existing_archived_tasks_and_with_created_user(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskAssociationModel))
    result: Optional[Row] = cursor.first()
    assert result is not None

    await async_connection.execute(
        update(
            TaskModel
        ).filter_by(
            id=FakeTaskConfig.ID
        ).values(
            is_archived=True
        )
    )

    await async_connection.execute(
        update(
            TaskAssociationModel
        ).filter_by(
            id=FakeTaskAssociationConfig.ID
        ).values(
            task_archived=True,
            task_completed=True
        )
    )
    await async_connection.commit()

    tasks: List[TaskModel] = [TaskModel(**FakeTaskConfig().to_dict(to_lower=True))]
    updated_tasks: List[TaskModel] = await update_tasks(tasks=tasks)
    assert len(updated_tasks) == 1
    task: TaskModel = updated_tasks[0]
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION
    assert task.is_archived is False

    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        cursor = await conn.execute(select(TaskAssociationModel))
        result = cursor.first()
        assert result is not None
        task_completed: bool = result[3]
        assert task_completed
        task_archived: bool = result[4]
        assert not task_archived


@pytest.mark.anyio
async def test_update_tasks_with_no_existing_tasks_and_no_users(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskModel))
    result: Optional[Row] = cursor.first()
    assert result is None

    cursor = await async_connection.execute(select(TaskAssociationModel))
    result = cursor.first()
    assert result is None

    tasks: List[TaskModel] = [TaskModel(**FakeTaskConfig().to_dict(to_lower=True))]
    updated_tasks: List[TaskModel] = await update_tasks(tasks=tasks)
    assert len(updated_tasks) == 1
    task: TaskModel = updated_tasks[0]
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION
    assert task.is_archived is False

    cursor = await async_connection.execute(select(TaskModel))
    result = cursor.first()
    assert result is not None

    cursor = await async_connection.execute(select(TaskAssociationModel))
    result = cursor.first()
    assert result is None


@pytest.mark.anyio
async def test_get_task_by_association_id_success(create_test_task: None) -> None:
    task: TaskModel = await get_task_by_association_id(task_association_id=FakeTaskAssociationConfig.ID)

    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_get_user_by_association_id_success(create_test_task: None) -> None:
    user: UserModel = await get_user_by_association_id(task_association_id=FakeTaskAssociationConfig.ID)

    assert user.id == FakeUserConfig.ID
    assert user.first_name == FakeUserConfig.FIRST_NAME


@pytest.mark.anyio
async def test_set_task_competed_for_user_success(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(
        select(
            TaskAssociationModel
        ).filter_by(
            id=FakeTaskAssociationConfig.ID
        )
    )
    result: Optional[Row] = cursor.first()
    assert result is not None
    task_completed: bool = result[3]
    assert not task_completed

    await set_task_competed_for_user(task_association_id=FakeTaskAssociationConfig.ID)

    cursor = await async_connection.execute(select(TaskAssociationModel).filter_by(id=FakeTaskAssociationConfig.ID))
    result = cursor.first()
    assert result is not None
    task_completed = result[3]
    assert task_completed
