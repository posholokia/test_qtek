from dataclasses import dataclass

from src.core.constructor.exceptions import BaseHttpException


@dataclass(eq=False)
class NotFoundDatabaseConfig(BaseHttpException):
    code: int = 500
    message: str = "Файл конфигурации для подключения к БД не найден"
