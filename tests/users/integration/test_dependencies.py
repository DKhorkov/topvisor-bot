import pytest
from typing import List, Optional
from aiogram.types import Message
from sqlalchemy import update, select, CursorResult, Row
from sqlalchemy.ext.asyncio import AsyncConnection

from src.users.constants import UserRoles
from src.users.exceptions import UserNotFoundError
from src.users.domain.models import UserModel
from tests.config import FakeUserConfig
from src.users.entrypoints.dependencies import (
    register_user,
    get_all_users,
    check_if_user_is_admin,
    get_user_by_id,
)


@pytest.mark.anyio
async def test_register_user_success_without_existing_user(
        map_models_to_orm: None,
        message: Message,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result: Optional[Row] = cursor.first()
    assert not result

    user: UserModel = await register_user(message=message)

    assert user.id == FakeUserConfig.ID
    assert user.username == FakeUserConfig.USERNAME
    assert user.first_name == FakeUserConfig.FIRST_NAME

    cursor = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result = cursor.first()
    assert result


@pytest.mark.anyio
async def test_register_user_success_with_existing_user(
        create_test_user: None,
        message: Message,
        async_connection: AsyncConnection
) -> None:

    cursor: CursorResult = await async_connection.execute(select(UserModel).filter_by(id=FakeUserConfig.ID))
    result: Optional[Row] = cursor.first()
    assert result

    user: UserModel = await register_user(message=message)

    assert user.id == FakeUserConfig.ID
    assert user.username == FakeUserConfig.USERNAME
    assert user.first_name == FakeUserConfig.FIRST_NAME


@pytest.mark.anyio
async def test_get_all_users_with_existing_user(create_test_user: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 1

    user: UserModel = users[0]
    assert user.id == FakeUserConfig.ID
    assert user.username == FakeUserConfig.USERNAME
    assert user.first_name == FakeUserConfig.FIRST_NAME
    assert user.url == FakeUserConfig.URL


@pytest.mark.anyio
async def test_get_all_users_without_existing_users(map_models_to_orm: None) -> None:
    users: List[UserModel] = await get_all_users()
    assert len(users) == 0


@pytest.mark.anyio
async def test_if_user_is_admin_with_default_role(create_test_user: None, message: Message) -> None:
    assert not await check_if_user_is_admin(message)


@pytest.mark.anyio
async def test_if_user_is_admin_with_admin_role(
        create_test_user: None,
        message: Message,
        async_connection: AsyncConnection
) -> None:

    await async_connection.execute(update(UserModel).values(role=UserRoles.ADMIN).filter_by(id=FakeUserConfig.ID))
    await async_connection.commit()

    assert await check_if_user_is_admin(message)


@pytest.mark.anyio
async def test_users_service_get_user_by_id_success(create_test_user: None) -> None:
    found_user: UserModel = await get_user_by_id(id=FakeUserConfig.ID)
    assert found_user.username == FakeUserConfig.USERNAME
    assert found_user.first_name == FakeUserConfig.FIRST_NAME
    assert found_user.id == FakeUserConfig.ID


@pytest.mark.anyio
async def test_users_service_get_user_by_id_fail(map_models_to_orm: None) -> None:
    with pytest.raises(UserNotFoundError):
        await get_user_by_id(id=FakeUserConfig.ID)
