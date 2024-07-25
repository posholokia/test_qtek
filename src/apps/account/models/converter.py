from .entity import UserEntity
from .sqla import UserModel


async def orm_user_to_dataclass(orm_obj: UserModel) -> UserEntity:
    return UserEntity(
        id=orm_obj.id,
        full_name=orm_obj.full_name,
    )
