from dataclasses import dataclass

from src.apps.account.exceptions.user import UserNotFoundError
from src.apps.account.models import (
    UserEntity,
    UserModel,
)
from src.apps.account.models.converter import orm_user_to_dataclass
from src.apps.account.repository.base import IUserRepository
from src.core.database.db import Database

from sqlalchemy import (
    delete,
    select,
    update,
)


@dataclass
class SQLAUserRepository(IUserRepository):
    db: Database

    async def create(self, full_name: str) -> UserEntity:
        async with self.db.get_session() as session:
            user = UserModel(
                full_name=full_name,
            )
            session.add(user)
            await session.commit()
            return await orm_user_to_dataclass(user)

    async def get_by_id(self, pk: int) -> UserEntity:
        async with self.db.get_session() as session:
            query = select(UserModel).where(UserModel.id == pk)
            cursor = await session.execute(query)
            user = cursor.fetchone()

            if user is None:
                raise UserNotFoundError()
            return await orm_user_to_dataclass(user[0])

    async def update(self, pk: int, **values) -> UserEntity:
        async with self.db.get_session() as session:
            query = (
                update(UserModel)
                .where(UserModel.id == pk)
                .values(**values)
                .returning(UserModel)
            )
            cursor = await session.execute(query)
            user = cursor.fetchone()

            if user is None:
                raise UserNotFoundError()
            return await orm_user_to_dataclass(user[0])

    async def delete(self, pk: int) -> None:
        async with self.db.get_session() as session:
            query = delete(UserModel).where(UserModel.id == pk)
            await session.execute(query)
            await session.commit()
