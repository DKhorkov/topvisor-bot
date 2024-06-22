from pydantic import BaseModel


class UserTasksStatisticsResponseScheme(BaseModel):
    description: str
    is_completed: bool
