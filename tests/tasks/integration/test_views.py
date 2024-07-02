import pytest
from typing import List

from src.tasks.domain.models import TaskModel
from src.tasks.entrypoints.schemas import UserTaskStatisticsResponseScheme
from src.tasks.interfaces import TasksUnitOfWork, TasksRepository, TasksAssociationsRepository
from src.tasks.entrypoints.views import TasksViews
from tests.config import FakeTaskConfig, FakeTaskAssociationConfig
from tests.tasks.fake_objects import FakeTasksUnitOfWork, FakeTasksRepository, FakeTasksAssociationsRepository
from tests.tasks.utils import (
    create_fake_tasks_associations_repository_instance,
    create_fake_tasks_repository_instance
)


@pytest.mark.anyio
async def test_tasks_views_get_all_tasks_with_existing_archived_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    assert isinstance(tasks_repository, FakeTasksRepository)
    tasks_repository.tasks[FakeTaskConfig.ID].is_archived = True

    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_views: TasksViews = TasksViews(uow=tasks_unit_of_work)
    tasks: List[TaskModel] = await tasks_views.get_all_tasks()
    assert len(tasks) == 0


@pytest.mark.anyio
async def test_tasks_views_get_all_tasks_without_existing_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_views: TasksViews = TasksViews(uow=tasks_unit_of_work)
    tasks: List[TaskModel] = await tasks_views.get_all_tasks()
    assert len(tasks) == 0


@pytest.mark.anyio
async def test_tasks_views_get_all_tasks_with_existing_non_archived_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_views: TasksViews = TasksViews(uow=tasks_unit_of_work)
    tasks: List[TaskModel] = await tasks_views.get_all_tasks()
    assert len(tasks) == 1

    task: TaskModel = tasks[0]
    assert task.id == FakeTaskConfig.ID
    assert not task.is_archived


@pytest.mark.anyio
async def test_tasks_views_get_user_tasks_statistics_with_existing_archived_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    assert isinstance(tasks_associations_repository, FakeTasksAssociationsRepository)
    tasks_associations_repository.tasks_associations[FakeTaskAssociationConfig.ID].task_archived = True

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_views: TasksViews = TasksViews(uow=tasks_unit_of_work)
    user_tasks_statistics: List[UserTaskStatisticsResponseScheme] = await tasks_views.get_user_tasks_statistics(
        user_id=FakeTaskAssociationConfig.USER_ID
    )

    assert len(user_tasks_statistics) == 0


@pytest.mark.anyio
async def test_tasks_views_get_user_tasks_statistics_without_existing_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_views: TasksViews = TasksViews(uow=tasks_unit_of_work)
    user_tasks_statistics: List[UserTaskStatisticsResponseScheme] = await tasks_views.get_user_tasks_statistics(
        user_id=FakeTaskAssociationConfig.USER_ID
    )

    assert len(user_tasks_statistics) == 0


@pytest.mark.anyio
async def test_tasks_views_get_user_tasks_statistics_with_existing_non_archived_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_views: TasksViews = TasksViews(uow=tasks_unit_of_work)
    user_tasks_statistics: List[UserTaskStatisticsResponseScheme] = await tasks_views.get_user_tasks_statistics(
        user_id=FakeTaskAssociationConfig.USER_ID
    )

    assert len(user_tasks_statistics) == 1

    task_statistics: UserTaskStatisticsResponseScheme = user_tasks_statistics[0]
    assert task_statistics.description == FakeTaskConfig.DESCRIPTION
    assert not task_statistics.is_completed
