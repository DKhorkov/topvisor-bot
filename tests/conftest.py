import pytest
from sqlalchemy import insert
from aiogram.types import Message
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy.exc import ArgumentError, IntegrityError
from typing import AsyncGenerator

from src.users.domain.models import UserModel
from src.core.database.connection import DATABASE_URL
from src.core.database.metadata import metadata
from src.users.adapters.orm import start_mappers as start_users_mappers
from src.tasks.adapters.orm import start_mappers as start_tasks_mappers
from src.tasks.domain.models import TaskModel, TaskAssociationModel
from tests.config import FakeUserConfig, FakeTaskConfig, FakeMessageConfig
from tests.utils import drop_test_db


@pytest.fixture(scope='session')
def anyio_backend() -> str:
    """
    Launch tests only on "asyncio" backend, without "trio" backend.
    """

    return 'asyncio'


@pytest.fixture
async def async_connection() -> AsyncGenerator[AsyncConnection, None]:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        yield conn


@pytest.fixture
async def create_test_db(async_connection: AsyncConnection) -> AsyncGenerator[None, None]:
    await async_connection.run_sync(metadata.create_all)
    yield
    drop_test_db()


@pytest.fixture
async def map_models_to_orm(create_test_db: None) -> None:
    """
    Create mappings from models to ORM according to DDD.
    """

    try:
        start_users_mappers()
        start_tasks_mappers()
    except ArgumentError:
        pass


@pytest.fixture
async def create_test_user(map_models_to_orm: None) -> None:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        try:
            await conn.execute(insert(UserModel).values(**FakeUserConfig().to_dict(to_lower=True)))
            await conn.commit()
        except IntegrityError:
            await conn.rollback()


@pytest.fixture
async def create_test_task(create_test_user: None) -> None:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        try:
            await conn.execute(insert(TaskModel).values(**FakeTaskConfig().to_dict(to_lower=True)))
            await conn.execute(
                insert(
                    TaskAssociationModel
                ).values(
                    task_id=FakeTaskConfig.ID,
                    user_id=FakeUserConfig.ID
                )
            )
            await conn.commit()
        except IntegrityError:
            await conn.rollback()


@pytest.fixture
async def message() -> Message:
    message: Message = Message(**FakeMessageConfig().to_dict(to_lower=True))
    return message
