import pytest
from typing import Optional, List, Sequence
from sqlalchemy import select, CursorResult, Row
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker

from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.adapters.repositories import SQLAlchemyTasksRepository, SQLAlchemyTasksAssociationsRepository
from tests.config import FakeTaskAssociationConfig, FakeTaskConfig


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_get_success(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task: Optional[TaskModel] = await SQLAlchemyTasksRepository(session=session).get(id=FakeTaskConfig.ID)

    assert task is not None
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_get_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task: Optional[TaskModel] = await SQLAlchemyTasksRepository(session=session).get(id=FakeTaskConfig.ID)
    assert task is None


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_get_by_description_success(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task: Optional[TaskModel] = await SQLAlchemyTasksRepository(session=session).get_by_description(
        description=FakeTaskConfig.DESCRIPTION
    )

    assert task is not None
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_get_by_description_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task: Optional[TaskModel] = await SQLAlchemyTasksRepository(session=session).get_by_description(
        description=FakeTaskConfig.DESCRIPTION
    )

    assert task is None


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_list(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    tasks_list: List[TaskModel] = await SQLAlchemyTasksRepository(session=session).list()
    assert len(tasks_list) == 1

    task: TaskModel = tasks_list[0]
    assert task.id == FakeTaskConfig.ID
    assert task.description == FakeTaskConfig.DESCRIPTION


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    tasks_list: List[TaskModel] = await SQLAlchemyTasksRepository(session=session).list()
    assert len(tasks_list) == 0


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_delete_existing_task(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyTasksRepository(session=session).delete(id=FakeTaskConfig.ID)

    cursor = await async_connection.execute(select(TaskModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_delete_non_existing_task(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyTasksRepository(session=session).delete(id=FakeTaskConfig.ID)


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_add_task_success(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskModel).filter_by(id=FakeTaskConfig.ID))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task: TaskModel = TaskModel(**FakeTaskConfig().to_dict(to_lower=True))
    await SQLAlchemyTasksRepository(session=session).add(model=task)

    cursor = await async_connection.execute(select(TaskModel).filter_by(id=FakeTaskConfig.ID))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_add_task_fail_already_exists(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskModel).filter_by(id=FakeTaskConfig.ID))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task: TaskModel = TaskModel(**FakeTaskConfig().to_dict(to_lower=True))
    with pytest.raises(IntegrityError):
        await SQLAlchemyTasksRepository(session=session).add(model=task)


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_update_existing_task(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskModel).filter_by(id=FakeTaskConfig.ID))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    fake_user_config: FakeTaskConfig = FakeTaskConfig()
    new_description: str = 'NewTaskDescription'
    fake_user_config.DESCRIPTION = new_description
    task: TaskModel = TaskModel(**fake_user_config.to_dict(to_lower=True))
    await SQLAlchemyTasksRepository(session=session).update(id=FakeTaskConfig.ID, model=task)

    cursor = await async_connection.execute(select(TaskModel).filter_by(id=FakeTaskConfig.ID))
    result = cursor.first()
    assert result
    assert result[1] == new_description


@pytest.mark.anyio
async def test_sqlalchemy_tasks_repository_update_non_existing_task(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskModel).filter_by(id=FakeTaskConfig.ID))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task: TaskModel = TaskModel(**FakeTaskConfig().to_dict(to_lower=True))
    with pytest.raises(NoResultFound):
        await SQLAlchemyTasksRepository(session=session).update(id=FakeTaskConfig.ID, model=task)


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_get_success(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task_association: Optional[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(
        session=session
    ).get(
        id=FakeTaskAssociationConfig.ID
    )

    assert task_association is not None
    assert task_association.id == FakeTaskAssociationConfig.ID
    assert task_association.user_id == FakeTaskAssociationConfig.USER_ID
    assert task_association.task_id == FakeTaskAssociationConfig.TASK_ID


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_get_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task_association: Optional[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(
        session=session
    ).get(
        id=FakeTaskAssociationConfig.ID
    )

    assert task_association is None


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_get_task_associations_by_task_id_success(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task_associations: List[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(
        session=session
    ).get_task_associations_by_task_id(
        task_id=FakeTaskAssociationConfig.TASK_ID
    )

    assert len(task_associations) == 1

    task_association: TaskAssociationModel = task_associations[0]
    assert task_association is not None
    assert task_association.id == FakeTaskAssociationConfig.ID
    assert task_association.user_id == FakeTaskAssociationConfig.USER_ID
    assert task_association.task_id == FakeTaskAssociationConfig.TASK_ID


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_get_task_associations_by_task_id_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task_associations: List[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(
        session=session
    ).get_task_associations_by_task_id(
        task_id=FakeTaskAssociationConfig.TASK_ID
    )

    assert len(task_associations) == 0


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_get_tasks_associations_by_user_id_success(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    tasks_associations: List[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(
        session=session
    ).get_tasks_associations_by_user_id(
        user_id=FakeTaskAssociationConfig.USER_ID
    )

    assert len(tasks_associations) == 1

    task_association: TaskAssociationModel = tasks_associations[0]
    assert task_association is not None
    assert task_association.id == FakeTaskAssociationConfig.ID
    assert task_association.user_id == FakeTaskAssociationConfig.USER_ID
    assert task_association.task_id == FakeTaskAssociationConfig.TASK_ID


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_get_tasks_associations_by_user_id_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    tasks_associations: List[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(
        session=session
    ).get_tasks_associations_by_user_id(
        user_id=FakeTaskAssociationConfig.USER_ID
    )

    assert len(tasks_associations) == 0


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_list(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    tasks_list: List[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(session=session).list()
    assert len(tasks_list) == 1

    task_association: TaskAssociationModel = tasks_list[0]
    assert task_association.id == FakeTaskAssociationConfig.ID
    assert task_association.user_id == FakeTaskAssociationConfig.USER_ID
    assert task_association.task_id == FakeTaskAssociationConfig.TASK_ID


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    tasks_list: List[TaskAssociationModel] = await SQLAlchemyTasksAssociationsRepository(session=session).list()
    assert len(tasks_list) == 0


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_delete_existing_task_association(
        create_test_task: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskAssociationModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyTasksAssociationsRepository(session=session).delete(id=FakeTaskAssociationConfig.ID)

    cursor = await async_connection.execute(select(TaskAssociationModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_delete_non_existing_task_association(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(TaskAssociationModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyTasksAssociationsRepository(session=session).delete(id=FakeTaskAssociationConfig.ID)


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_add_task_association_success(
        map_models_to_orm: None,
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
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task_association: TaskAssociationModel = TaskAssociationModel(**FakeTaskAssociationConfig().to_dict(to_lower=True))
    await SQLAlchemyTasksAssociationsRepository(session=session).add(model=task_association)

    cursor = await async_connection.execute(select(TaskAssociationModel).filter_by(id=FakeTaskAssociationConfig.ID))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_update_existing_task_association(
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
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    fake_user_config: FakeTaskAssociationConfig = FakeTaskAssociationConfig()
    fake_user_config.TASK_COMPLETED = True
    task_association: TaskAssociationModel = TaskAssociationModel(**fake_user_config.to_dict(to_lower=True))
    await SQLAlchemyTasksAssociationsRepository(
        session=session
    ).update(
        id=FakeTaskAssociationConfig.ID,
        model=task_association
    )

    cursor = await async_connection.execute(select(TaskAssociationModel).filter_by(id=FakeTaskAssociationConfig.ID))
    result = cursor.first()
    assert result
    assert result[3] is True


@pytest.mark.anyio
async def test_sqlalchemy_tasks_associations_repository_update_non_existing_task_association(
        map_models_to_orm: None,
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
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    task_association: TaskAssociationModel = TaskAssociationModel(**FakeTaskAssociationConfig().to_dict(to_lower=True))
    with pytest.raises(NoResultFound):
        await SQLAlchemyTasksAssociationsRepository(
            session=session
        ).update(
            id=FakeTaskAssociationConfig.ID,
            model=task_association
        )
