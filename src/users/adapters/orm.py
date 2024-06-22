from sqlalchemy import Table, Column, String, DateTime, Boolean, BigInteger
from datetime import datetime, timezone

from src.core.database.metadata import mapper_registry


users_table = Table(
    'users',
    mapper_registry.metadata,
    Column('id', BigInteger, primary_key=True, nullable=False, unique=True),
    Column('is_bot', Boolean, nullable=False),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=True),
    Column('username', String, nullable=True),
    Column('role', String, nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc)),
    Column(
        'updated_at',
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )
)


def start_mappers():
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """

    # Imports here not to ruin alembic logics. Also, only for mappers they needed:
    from src.users.domain.models import UserModel

    mapper_registry.map_imperatively(class_=UserModel, local_table=users_table)
