from dataclasses import dataclass

from src.core.constructor.exceptions import BaseHttpException


@dataclass(eq=False)
class UserNotFoundError(BaseHttpException):
    code: int = 400
    message: str = "Пользователь не найден"
