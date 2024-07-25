from dataclasses import dataclass

from src.apps.account.models import UserEntity
from src.apps.account.repository.base import IUserRepository


@dataclass
class UserAction:
    repository: IUserRepository

    async def get_user_by_id(self, pk: int) -> UserEntity:
        return await self.repository.get_by_id(pk)

    async def create_user(self, full_name: str) -> UserEntity:
        return await self.repository.create(full_name)

    async def delete_user(self, pk: int) -> None:
        return await self.repository.delete(pk)

    async def update_user(self, pk: int, full_name: str) -> UserEntity:
        return await self.repository.update(pk, full_name=full_name)
