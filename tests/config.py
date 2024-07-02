from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any
from aiogram.types import User, Chat

from src.users.constants import UserRoles


@dataclass
class BaseTestConfig:

    def to_dict(self, to_lower: bool = False) -> Dict[str, Any]:
        base_dict: Dict[str, Any] = asdict(self)
        if to_lower:
            return {k.lower(): v for k, v in base_dict.items()}

        return base_dict


@dataclass
class FakeUserConfig(BaseTestConfig):
    ID: int = 1
    IS_BOT: bool = False
    USERNAME: str = 'test_username'
    LAST_NAME: str = 'fake_last_name'
    FIRST_NAME: str = 'fake_first_name'
    FULL_NAME: str = 'fake_full_name'
    URL: str = 'http://fake_url'
    ROLE: str = UserRoles.DEFAULT


@dataclass
class FakeTaskConfig(BaseTestConfig):
    ID: int = 1
    DESCRIPTION: str = 'test_task'


@dataclass
class FakeTaskAssociationConfig(BaseTestConfig):
    ID: int = 1
    TASK_ID: int = FakeTaskConfig.ID
    USER_ID: int = FakeUserConfig.ID
    TASK_ARCHIVED: bool = False
    TASK_COMPLETED: bool = False


@dataclass
class FakeChatConfig(BaseTestConfig):
    ID: int = 1
    TYPE: str = 'private'


@dataclass
class FakeMessageConfig(BaseTestConfig):
    CHAT: Chat = Chat(**FakeChatConfig().to_dict(to_lower=True))
    DATE: datetime = datetime.now()
    MESSAGE_ID: int = 1
    FROM_USER: User = User(**FakeUserConfig().to_dict(to_lower=True))
