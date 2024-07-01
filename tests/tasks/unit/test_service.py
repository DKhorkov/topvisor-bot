import pytest
from typing import List

from src.tasks.constants import ErrorDetails
from src.tasks.exceptions import TaskNotFoundError, TaskAssociationNotFoundError
from src.tasks.interfaces.repositories import TasksRepository, TasksAssociationsRepository
from src.tasks.interfaces.units_of_work import TasksUnitOfWork
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.service_layer.service import TasksService
from src.users.domain.models import UserModel
from tests.tasks.fake_objects import FakeTasksUnitOfWork, FakeTasksRepository, FakeTasksAssociationsRepository
from tests.config import FakeTaskConfig, FakeTaskAssociationConfig, FakeUserConfig
from tests.tasks.utils import (
    create_fake_tasks_associations_repository_instance,
    create_fake_tasks_repository_instance
)


@pytest.mark.anyio
async def test_tasks_service_create_task_without_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )
    
    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 0
    assert len(await tasks_associations_repository.list()) == 0
    task: TaskModel = TaskModel(**FakeTaskConfig().to_dict(to_lower=True))
    await tasks_service.create_task(task=task, users=[])
    assert len(await tasks_repository.list()) == 1
    assert len(await tasks_associations_repository.list()) == 0


@pytest.mark.anyio
async def test_tasks_service_create_task_with_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 0
    assert len(await tasks_associations_repository.list()) == 0
    task: TaskModel = TaskModel(**FakeTaskConfig().to_dict(to_lower=True))
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    await tasks_service.create_task(task=task, users=[user])
    assert len(await tasks_repository.list()) == 1
    assert len(await tasks_associations_repository.list()) == 1


@pytest.mark.anyio
async def test_tasks_service_get_task_by_id_success() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 1
    found_task: TaskModel = await tasks_service.get_task_by_id(id=FakeTaskConfig.ID)
    assert found_task.id == FakeTaskConfig.ID
    assert found_task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_tasks_service_get_task_by_id_fail() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 0
    with pytest.raises(TaskNotFoundError):
        await tasks_service.get_task_by_id(id=FakeTaskConfig.ID)


@pytest.mark.anyio
async def test_tasks_service_get_task_by_description_success() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 1
    found_task: TaskModel = await tasks_service.get_task_by_description(description=FakeTaskConfig.DESCRIPTION)
    assert found_task.id == FakeTaskConfig.ID
    assert found_task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_tasks_service_get_task_by_description_fail() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 0
    with pytest.raises(TaskNotFoundError):
        await tasks_service.get_task_by_description(description=FakeTaskConfig.DESCRIPTION)


@pytest.mark.anyio
async def test_tasks_service_check_task_existence_success_by_id() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 1
    assert await tasks_service.check_task_existence(id=FakeTaskConfig.ID)


@pytest.mark.anyio
async def test_tasks_service_check_task_existence_success_by_description() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 1
    assert await tasks_service.check_task_existence(description=FakeTaskConfig.DESCRIPTION)


@pytest.mark.anyio
async def test_tasks_service_check_task_existence_fail_task_does_not_exist() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 0
    assert not await tasks_service.check_task_existence(id=FakeTaskConfig.ID)


@pytest.mark.anyio
async def test_tasks_service_check_task_existence_fail_no_attributes_provided() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    with pytest.raises(ValueError) as exc_info:
        await tasks_service.check_task_existence()

    assert str(exc_info.value) == ErrorDetails.TASK_ATTRIBUTE_REQUIRED


@pytest.mark.anyio
async def test_tasks_service_get_all_tasks_with_existing_task() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    tasks: List[TaskModel] = await tasks_service.get_all_tasks()
    assert len(tasks) == 1

    task: TaskModel = tasks[0]
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_tasks_service_get_all_tasks_without_existing_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    tasks: List[TaskModel] = await tasks_service.get_all_tasks()
    assert len(tasks) == 0


@pytest.mark.anyio
async def test_tasks_service_create_tasks_associations_for_user() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 1
    assert len(await tasks_associations_repository.list()) == 0
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    await tasks_service.create_tasks_associations_for_user(user=user)
    assert len(await tasks_repository.list()) == 1
    assert len(await tasks_associations_repository.list()) == 1


@pytest.mark.anyio
async def test_tasks_service_get_user_tasks_associations_with_existing_tasks_associations() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_associations_repository.list()) == 1
    tasks_associations: List[TaskAssociationModel] = await tasks_service.get_user_tasks_associations(user_id=1)
    assert len(tasks_associations) == 1

    task_association: TaskAssociationModel = tasks_associations[0]
    assert task_association.id == FakeTaskAssociationConfig.ID
    assert task_association.user_id == FakeTaskAssociationConfig.USER_ID
    assert task_association.task_id == FakeTaskAssociationConfig.TASK_ID


@pytest.mark.anyio
async def test_tasks_service_get_user_tasks_associations_without_existing_tasks_associations() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_associations_repository.list()) == 0
    tasks_associations: List[TaskAssociationModel] = await tasks_service.get_user_tasks_associations(user_id=1)
    assert len(tasks_associations) == 0


@pytest.mark.anyio
async def test_tasks_service_archive_old_tasks_with_new_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 1
    assert not (await tasks_repository.list())[0].is_archived
    assert len(await tasks_associations_repository.list()) == 1
    assert not (await tasks_associations_repository.list())[0].task_archived

    new_task: TaskModel = TaskModel(**FakeTaskConfig().to_dict(to_lower=True))
    await tasks_service.archive_old_tasks(new_tasks=[new_task])

    # Task is equal to existing, so existing task should not be archived:
    assert len(await tasks_repository.list()) == 1
    assert not (await tasks_repository.list())[0].is_archived
    assert len(await tasks_associations_repository.list()) == 1
    assert not (await tasks_associations_repository.list())[0].task_archived


@pytest.mark.anyio
async def test_tasks_service_archive_old_tasks_without_new_tasks() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert len(await tasks_repository.list()) == 1
    assert not (await tasks_repository.list())[0].is_archived
    assert len(await tasks_associations_repository.list()) == 1
    assert not (await tasks_associations_repository.list())[0].task_archived

    await tasks_service.archive_old_tasks(new_tasks=[])

    assert len(await tasks_repository.list()) == 1
    assert (await tasks_repository.list())[0].is_archived
    assert len(await tasks_associations_repository.list()) == 1
    assert (await tasks_associations_repository.list())[0].task_archived


@pytest.mark.anyio
async def test_tasks_service_reopen_task_success() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)

    assert isinstance(tasks_repository, FakeTasksRepository)
    tasks_repository.tasks[FakeTaskConfig.ID].is_archived = True
    assert (await tasks_repository.list())[0].is_archived

    assert isinstance(tasks_associations_repository, FakeTasksAssociationsRepository)
    tasks_associations_repository.tasks_associations[FakeTaskAssociationConfig.ID].task_archived = True
    assert (await tasks_associations_repository.list())[0].task_archived

    task: TaskModel = await tasks_service.reopen_task(id=FakeTaskConfig.ID)
    assert task.id == FakeTaskConfig.ID
    assert task.is_archived is False

    assert not (await tasks_repository.list())[0].is_archived
    assert not (await tasks_associations_repository.list())[0].task_archived


@pytest.mark.anyio
async def test_tasks_service_reopen_task_fail() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    with pytest.raises(TaskNotFoundError):
        await tasks_service.reopen_task(id=FakeTaskConfig.ID)


@pytest.mark.anyio
async def test_tasks_service_get_task_by_association_id_success() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    task: TaskModel = await tasks_service.get_task_by_association_id(task_association_id=FakeTaskAssociationConfig.ID)
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_tasks_service_get_task_by_association_id_fail_task_association_does_not_exist() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    with pytest.raises(TaskAssociationNotFoundError):
        await tasks_service.get_task_by_association_id(task_association_id=FakeTaskAssociationConfig.ID)


@pytest.mark.anyio
async def test_tasks_service_get_task_by_association_id_fail_task_does_not_exist() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    with pytest.raises(TaskNotFoundError):
        await tasks_service.get_task_by_association_id(task_association_id=FakeTaskAssociationConfig.ID)


@pytest.mark.anyio
async def test_tasks_service_get_task_association_by_id_success() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    task_association: TaskAssociationModel = await tasks_service.get_task_association_by_id(
        task_association_id=FakeTaskAssociationConfig.ID
    )

    assert task_association.id == FakeTaskAssociationConfig.ID
    assert task_association.task_id == FakeTaskAssociationConfig.TASK_ID
    assert task_association.user_id == FakeTaskAssociationConfig.USER_ID


@pytest.mark.anyio
async def test_tasks_service_get_task_association_by_id_fail_task_association_does_not_exist() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    with pytest.raises(TaskAssociationNotFoundError):
        await tasks_service.get_task_association_by_id(
            task_association_id=FakeTaskAssociationConfig.ID
        )


@pytest.mark.anyio
async def test_tasks_service_set_task_association_completed_status_success() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance(with_task=True)
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance(with_tasks_associations=True)
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    assert isinstance(tasks_associations_repository, FakeTasksAssociationsRepository)
    assert not (await tasks_associations_repository.list())[0].task_completed

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    task_association: TaskAssociationModel = await tasks_service.set_task_association_completed_status(
        task_association_id=FakeTaskAssociationConfig.ID
    )

    assert task_association.id == FakeTaskAssociationConfig.ID
    assert task_association.task_id == FakeTaskAssociationConfig.TASK_ID
    assert task_association.user_id == FakeTaskAssociationConfig.USER_ID
    assert task_association.task_completed

    assert (await tasks_associations_repository.list())[0].task_completed


@pytest.mark.anyio
async def test_tasks_service_set_task_association_completed_status_fail_task_association_does_not_exist() -> None:
    tasks_repository: TasksRepository = await create_fake_tasks_repository_instance()
    tasks_associations_repository: TasksAssociationsRepository = (
        await create_fake_tasks_associations_repository_instance()
    )

    tasks_unit_of_work: TasksUnitOfWork = FakeTasksUnitOfWork(
        tasks_repository=tasks_repository,
        tasks_associations_repository=tasks_associations_repository
    )

    tasks_service: TasksService = TasksService(uow=tasks_unit_of_work)
    with pytest.raises(TaskAssociationNotFoundError):
        await tasks_service.set_task_association_completed_status(
            task_association_id=FakeTaskAssociationConfig.ID
        )
