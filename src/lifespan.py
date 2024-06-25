from sqlalchemy.orm import clear_mappers

from src.users.adapters.orm import start_mappers as start_users_mappers
from src.tasks.adapters.orm import start_mappers as start_tasks_mappers


def on_startup() -> None:
    start_users_mappers()
    start_tasks_mappers()


def on_shutdown() -> None:
    clear_mappers()
