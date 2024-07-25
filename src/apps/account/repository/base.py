from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from src.apps.account.models import UserEntity


@dataclass
class IUserRepository(ABC):
    @abstractmethod
    async def create(self, full_name: str) -> UserEntity: ...

    @abstractmethod
    async def get_by_id(self, pk: int) -> UserEntity: ...

    @abstractmethod
    async def update(self, pk: int, **values) -> UserEntity: ...

    @abstractmethod
    async def delete(self, pk: int) -> None: ...
