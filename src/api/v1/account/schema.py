from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    full_name: str


class CreateUserSchema(BaseUserSchema):
    pass


class RetrieveUserSchema(BaseUserSchema):
    id: int


class UpdateUserSchema(BaseUserSchema):
    pass
