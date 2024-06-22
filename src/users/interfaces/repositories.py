from typing import Optional, List
from abc import ABC, abstractmethod

from src.core.interfaces import AbstractRepository, AbstractModel
from src.users.domain.models import UserModel


class UsersRepository(AbstractRepository, ABC):
    """
    An interface for work with users, that is used by users unit of work of the authorization module.
    The main goal is that implementations of this interface can be easily replaced in the users unit of work of
    the authorization module using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    async def get_by_first_name(self, first_name: str) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: AbstractModel) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> Optional[UserModel]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, model: AbstractModel) -> UserModel:
        raise NotImplementedError

    @abstractmethod
    async def list(self) -> List[UserModel]:
        raise NotImplementedError
