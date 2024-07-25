from functools import lru_cache

from punq import Container
from src.apps.account.actions import UserAction
from src.apps.account.repository.base import IUserRepository
from src.apps.account.repository.memory import MemoryUserRepository
from src.apps.account.repository.sqla import SQLAUserRepository
from src.core.database.db import (
    Database,
    RepositoryType,
)


@lru_cache(1)
def get_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container: Container = Container()

    def build_user_repository() -> MemoryUserRepository | SQLAUserRepository:
        # репозиторий билдится в зависимости от типа хранения данных
        db = container.resolve(Database)

        if db.repository_type == RepositoryType.memory:
            return MemoryUserRepository()
        elif db.repository_type == RepositoryType.postgres:
            return SQLAUserRepository(db)

    container.register(Database, instance=Database.build())

    container.register(IUserRepository, factory=build_user_repository)

    container.register(UserAction)
    return container
