from sqlalchemy import Table, Column, String, DateTime, Boolean, Integer, ForeignKey
from datetime import datetime, timezone

from src.core.database.metadata import mapper_registry


tasks_table = Table(
    'tasks',
    mapper_registry.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True, nullable=False, unique=True),
    Column('description', String, nullable=False),
    Column('is_archived', Boolean, nullable=False, default=False),
    Column('created_at', DateTime(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc)),
    Column(
        'updated_at',
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc)
    )
)


tasks_associations_table = Table(
    'tasks_associations',
    mapper_registry.metadata,
    Column('id', Integer, autoincrement=True, primary_key=True, nullable=False, unique=True),
    Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('task_completed', Boolean, nullable=False, default=False),
    Column('task_archived', Boolean, nullable=False, default=False)
)


def start_mappers():
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """

    # Imports here not to ruin alembic logics. Also, only for mappers they needed:
    from src.tasks.domain.models import TaskModel, TaskAssociationModel

    mapper_registry.map_imperatively(class_=TaskModel, local_table=tasks_table)
    mapper_registry.map_imperatively(class_=TaskAssociationModel, local_table=tasks_associations_table)
