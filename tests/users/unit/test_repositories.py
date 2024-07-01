import pytest
from typing import Optional, List, Sequence
from sqlalchemy import select, CursorResult, Row
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker

from src.users.domain.models import UserModel
from src.users.adapters.repositories import SQLAlchemyUsersRepository
from tests.config import FakeUserConfig


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get(id=FakeUserConfig.ID)

    assert user is not None
    assert user.id == FakeUserConfig.ID
    assert user.first_name == FakeUserConfig.FIRST_NAME
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get(id=FakeUserConfig.ID)
    assert user is None


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_first_name_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_first_name(
        first_name=FakeUserConfig.FIRST_NAME
    )

    assert user is not None
    assert user.id == FakeUserConfig.ID
    assert user.first_name == FakeUserConfig.FIRST_NAME
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_first_name_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_first_name(
        first_name=FakeUserConfig.FIRST_NAME
    )

    assert user is None


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_username_success(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_username(
        username=FakeUserConfig.USERNAME
    )

    assert user is not None
    assert user.id == FakeUserConfig.ID
    assert user.first_name == FakeUserConfig.FIRST_NAME
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_get_by_username_fail(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: Optional[UserModel] = await SQLAlchemyUsersRepository(session=session).get_by_username(
        username=FakeUserConfig.USERNAME
    )

    assert user is None


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_list(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_list: List[UserModel] = await SQLAlchemyUsersRepository(session=session).list()
    assert len(users_list) == 1

    user: UserModel = users_list[0]
    assert user.id == FakeUserConfig.ID
    assert user.first_name == FakeUserConfig.FIRST_NAME
    assert user.username == FakeUserConfig.USERNAME


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_empty_list(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    users_list: List[UserModel] = await SQLAlchemyUsersRepository(session=session).list()
    assert len(users_list) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_delete_existing_user(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 1

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersRepository(session=session).delete(id=FakeUserConfig.ID)

    cursor = await async_connection.execute(select(UserModel))
    result = cursor.all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_delete_non_existing_user(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel))
    result: Sequence[Row] = cursor.all()
    assert len(result) == 0

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    await SQLAlchemyUsersRepository(session=session).delete(id=FakeUserConfig.ID)


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_add_user_success(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    await SQLAlchemyUsersRepository(session=session).add(model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_add_user_fail_id_already_exists(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(IntegrityError):
        await SQLAlchemyUsersRepository(session=session).add(model=user)


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_update_existing_user(
        create_test_user: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result: Optional[Row] = cursor.first()
    assert result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    fake_user_config: FakeUserConfig = FakeUserConfig()
    new_username: str = 'someUsername'
    fake_user_config.USERNAME = new_username
    user: UserModel = UserModel(**fake_user_config.to_dict(to_lower=True))
    await SQLAlchemyUsersRepository(session=session).update(id=FakeUserConfig.ID, model=user)

    cursor = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result = cursor.first()
    assert result
    assert result[6] == new_username


@pytest.mark.anyio
async def test_sqlalchemy_users_repository_update_non_existing_user(
        map_models_to_orm: None,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result: Optional[Row] = cursor.first()
    assert not result

    async_session_factory: async_sessionmaker = async_sessionmaker(bind=async_connection)
    session: AsyncSession = async_session_factory()
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    with pytest.raises(NoResultFound):
        await SQLAlchemyUsersRepository(session=session).update(id=FakeUserConfig.ID, model=user)
