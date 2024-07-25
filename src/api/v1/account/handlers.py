from punq import Container
from src.api.v1.account.schema import (
    CreateUserSchema,
    RetrieveUserSchema,
    UpdateUserSchema,
)
from src.apps.account.actions import UserAction
from src.apps.account.models import UserEntity
from src.config.containers import get_container
from src.core.mapper import Mapper

from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status


router = APIRouter()


@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUserSchema = Depends(),
    container: Container = Depends(get_container),
) -> RetrieveUserSchema:
    """Создать юзера"""
    action: UserAction = container.resolve(UserAction)
    user: UserEntity = await action.create_user(
        full_name=user_data.full_name,
    )
    return Mapper.dataclass_to_schema(RetrieveUserSchema, user)


@router.get("/user/{pk}/", status_code=status.HTTP_200_OK)
async def get_user(
    pk: int,
    container: Container = Depends(get_container),
) -> RetrieveUserSchema:
    """Получить юзера"""
    action: UserAction = container.resolve(UserAction)
    user: UserEntity = await action.get_user_by_id(pk)
    return Mapper.dataclass_to_schema(RetrieveUserSchema, user)


@router.patch("/user/{pk}/", status_code=status.HTTP_200_OK)
async def update_user(
    pk: int,
    user_data: UpdateUserSchema,
    container: Container = Depends(get_container),
) -> RetrieveUserSchema:
    """Изменение юзера"""
    action: UserAction = container.resolve(UserAction)
    user: UserEntity = await action.update_user(
        pk=pk,
        full_name=user_data.full_name,
    )

    return Mapper.dataclass_to_schema(RetrieveUserSchema, user)


@router.delete("/user/{pk}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    pk: int,
    container: Container = Depends(get_container),
) -> None:
    """Удаление юзера"""
    action: UserAction = container.resolve(UserAction)
    await action.delete_user(pk)
    return None
