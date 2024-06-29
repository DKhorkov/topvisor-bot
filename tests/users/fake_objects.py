from typing import Dict, Optional, List

from src.users.interfaces.units_of_work import UsersUnitOfWork
from src.users.interfaces.repositories import UsersRepository
from src.users.domain.models import UserModel
from src.core.interfaces import AbstractModel


class FakeUsersRepository(UsersRepository):

    def __init__(self, users: Optional[Dict[int, UserModel]] = None) -> None:
        self.users: Dict[int, UserModel] = users if users else {}

    async def get_by_first_name(self, first_name: str) -> Optional[UserModel]:
        for user in self.users.values():
            if user.first_name == first_name:
                return user

        return None

    async def get(self, id: int) -> Optional[UserModel]:
        return self.users.get(id)

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        for user in self.users.values():
            if user.username == username:
                return user

        return None

    async def add(self, model: AbstractModel) -> UserModel:
        user: UserModel = UserModel(**await model.to_dict())
        self.users[user.id] = user
        return user

    async def update(self, id: int, model: AbstractModel) -> UserModel:
        user: UserModel = UserModel(**await model.to_dict())
        if id in self.users:
            self.users[id] = user

        return user

    async def delete(self, id: int) -> None:
        if id in self.users:
            del self.users[id]

    async def list(self) -> List[UserModel]:
        return list(self.users.values())


class FakeUsersUnitOfWork(UsersUnitOfWork):

    def __init__(self, users_repository: UsersRepository) -> None:
        super().__init__()
        self.users: UsersRepository = users_repository
        self.committed: bool = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        pass
