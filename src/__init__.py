# Importing all tables for alembic autogenerate correct work:
from src.users.adapters.orm import users_table
from src.tasks.adapters.orm import tasks_table, tasks_associations_table
