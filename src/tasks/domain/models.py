from dataclasses import dataclass
from typing import Any

from src.core.interfaces import AbstractModel


@dataclass
class TaskModel(AbstractModel):
    description: str
    is_archived: bool = False
    id: int = 0

    def __hash__(self) -> int:
        return hash(self.description)

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)


@dataclass
class TaskAssociationModel(AbstractModel):
    user_id: int
    task_id: int
    task_completed: bool = False
    task_archived: bool = False
    id: int = 0

    def __hash__(self) -> int:
        return hash(f'{self.user_id}_{self.task_id}')

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)
