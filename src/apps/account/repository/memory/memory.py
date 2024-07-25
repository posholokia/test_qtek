import collections
from dataclasses import dataclass

from src.apps.account.exceptions.user import UserNotFoundError
from src.apps.account.models import UserEntity
from src.apps.account.repository.base import IUserRepository

from .mock import user_data


@dataclass
class MemoryUserRepository(IUserRepository):
    async def create(self, full_name: str) -> UserEntity:
        # получаем значение последнего id в списке
        # работает в > 3.7
        last_id = collections.deque(user_data, maxlen=1)
        # если список пуст, то id=1, иначе прибавляем 1 к последнему
        user_pk = last_id[0] + 1 if last_id else 1
        user = UserEntity(
            id=user_pk,
            full_name=full_name,
        )
        user_data.update({user_pk: user})

        return user

    async def get_by_id(self, pk: int) -> UserEntity:
        user = user_data.get(pk)

        if user is None:
            raise UserNotFoundError()

        return user

    async def update(self, pk: int, **values) -> UserEntity:
        user = await self.get_by_id(pk)
        for key, value in values.items():
            if hasattr(user, key) and key != "id":
                setattr(user, key, value)

        return user

    async def delete(self, pk: int) -> None:
        try:
            user_data.pop(pk)
        except KeyError:
            raise UserNotFoundError()
