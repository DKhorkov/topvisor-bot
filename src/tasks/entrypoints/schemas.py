from pydantic import BaseModel


class UserTaskStatisticsResponseScheme(BaseModel):
    description: str
    is_completed: bool


class UserActiveTaskScheme(BaseModel):
    task_association_id: int
    description: str
