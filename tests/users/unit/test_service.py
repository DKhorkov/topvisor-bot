import pytest
from typing import List

from src.users.constants import ErrorDetails
from src.users.exceptions import UserNotFoundError
from src.users.interfaces.repositories import UsersRepository
from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.domain.models import UserModel
from src.users.service_layer.service import UsersService
from tests.users.fake_objects import FakeUsersUnitOfWork
from tests.config import FakeUserConfig
from tests.users.utils import create_fake_users_repository_instance


@pytest.mark.anyio
async def test_users_service_register_user_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
    await users_service.register_user(user=user)
    assert len(await users_repository.list()) == 1


@pytest.mark.anyio
async def test_users_service_get_user_by_id_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_id(id=FakeUserConfig.ID)
    assert found_user.username == FakeUserConfig.USERNAME
    assert found_user.first_name == FakeUserConfig.FIRST_NAME
    assert found_user.id == FakeUserConfig.ID


@pytest.mark.anyio
async def test_users_service_get_user_by_id_fail() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_id(id=FakeUserConfig.ID)


@pytest.mark.anyio
async def test_users_service_get_user_by_first_name_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_first_name(first_name=FakeUserConfig.FIRST_NAME)
    assert found_user.username == FakeUserConfig.USERNAME
    assert found_user.first_name == FakeUserConfig.FIRST_NAME
    assert found_user.id == FakeUserConfig.ID


@pytest.mark.anyio
async def test_users_service_get_user_by_first_name_fail() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_first_name(first_name=FakeUserConfig.FIRST_NAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_id() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(id=FakeUserConfig.ID)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_first_name() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(first_name=FakeUserConfig.FIRST_NAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_success_by_username() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    assert await users_service.check_user_existence(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_user_does_not_exist() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    assert not await users_service.check_user_existence(id=FakeUserConfig.ID)


@pytest.mark.anyio
async def test_users_service_check_user_existence_fail_no_attributes_provided() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)
    with pytest.raises(ValueError) as exc_info:
        await users_service.check_user_existence()

    assert str(exc_info.value) == ErrorDetails.USER_ATTRIBUTE_REQUIRED


@pytest.mark.anyio
async def test_users_service_get_user_by_username_success() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 1
    found_user: UserModel = await users_service.get_user_by_username(username=FakeUserConfig.USERNAME)
    assert found_user.username == FakeUserConfig.USERNAME
    assert found_user.first_name == FakeUserConfig.FIRST_NAME
    assert found_user.id == FakeUserConfig.ID


@pytest.mark.anyio
async def test_users_service_get_user_by_username_fail() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    assert len(await users_repository.list()) == 0
    with pytest.raises(UserNotFoundError):
        await users_service.get_user_by_username(username=FakeUserConfig.USERNAME)


@pytest.mark.anyio
async def test_users_service_get_all_users_with_existing_user() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance(with_user=True)
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    users: List[UserModel] = await users_service.get_all_users()
    assert len(users) == 1

    user: UserModel = users[0]
    assert user.username == FakeUserConfig.USERNAME
    assert user.first_name == FakeUserConfig.FIRST_NAME
    assert user.id == FakeUserConfig.ID


@pytest.mark.anyio
async def test_users_service_get_all_users_without_existing_users() -> None:
    users_repository: UsersRepository = await create_fake_users_repository_instance()
    users_unit_of_work: UsersUnitOfWork = FakeUsersUnitOfWork(users_repository=users_repository)
    users_service: UsersService = UsersService(uow=users_unit_of_work)

    users: List[UserModel] = await users_service.get_all_users()
    assert len(users) == 0
