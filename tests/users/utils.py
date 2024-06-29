from src.users.domain.models import UserModel
from src.users.interfaces import UsersRepository
from tests.config import FakeUserConfig
from tests.users.fake_objects import FakeUsersRepository


async def create_fake_users_repository_instance(with_user: bool = False) -> UsersRepository:
    users_repository: UsersRepository
    if with_user:
        user: UserModel = UserModel(**FakeUserConfig().to_dict(to_lower=True))
        users_repository = FakeUsersRepository(users={FakeUserConfig.ID: user})
    else:
        users_repository = FakeUsersRepository()

    return users_repository
