import os
from random import choice
from string import ascii_uppercase

from src.core.database.config import database_config


def drop_test_db() -> None:
    if os.path.exists(database_config.DATABASE_NAME):
        os.remove(database_config.DATABASE_NAME)


def generate_random_string(length: int) -> str:
    return ''.join(choice(ascii_uppercase) for _ in range(length))
