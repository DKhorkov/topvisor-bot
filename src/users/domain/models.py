from dataclasses import dataclass
from typing import Any, Optional

from src.core.interfaces import AbstractModel


@dataclass
class UserModel(AbstractModel):
    id: int
    is_bot: bool
    first_name: str
    role: str
    full_name: str
    url: str
    last_name: Optional[str] = None
    username: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)
