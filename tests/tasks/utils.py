from src.tasks.domain.models import TaskModel, TaskAssociationModel
from src.tasks.interfaces import TasksRepository, TasksAssociationsRepository
from tests.config import FakeTaskConfig, FakeTaskAssociationConfig
from tests.tasks.fake_objects import FakeTasksRepository, FakeTasksAssociationsRepository


async def create_fake_tasks_repository_instance(with_task: bool = False) -> TasksRepository:
    tasks_repository: TasksRepository
    if with_task:
        task: TaskModel = TaskModel(**FakeTaskConfig().to_dict(to_lower=True))
        tasks_repository = FakeTasksRepository(tasks={FakeTaskConfig.ID: task})
    else:
        tasks_repository = FakeTasksRepository()

    return tasks_repository


async def create_fake_tasks_associations_repository_instance(
        with_tasks_associations: bool = False
) -> TasksAssociationsRepository:

    tasks_associations_repository: TasksAssociationsRepository
    if with_tasks_associations:
        task_association: TaskAssociationModel = TaskAssociationModel(
            **FakeTaskAssociationConfig().to_dict(to_lower=True)
        )

        tasks_associations_repository = FakeTasksAssociationsRepository(
            tasks_associations={
                FakeTaskAssociationConfig.ID: task_association
            }
        )
    else:
        tasks_associations_repository = FakeTasksAssociationsRepository()

    return tasks_associations_repository
