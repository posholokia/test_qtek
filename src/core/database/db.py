import json
from contextlib import asynccontextmanager
from enum import Enum
from typing import (
    Any,
    AsyncGenerator,
)

from loguru import logger
from src.config import settings
from src.core.database.conf import PostgresConf

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from src.core.database.exceptions import NotFoundDatabaseConfig

Base = declarative_base()


class RepositoryType(Enum):
    memory: str = "memory"  # данные хранятся в памяти
    postgres: str = "postgres"  # данные в postgresql


class Database:
    # ссылка подключения к БД. None для репозитория в памяти
    url: str | None = None
    # тип репозитория
    repository_type: RepositoryType = RepositoryType.memory

    @classmethod
    def build(cls) -> "Database":
        # билдит подключение к БД из конфиг файла
        try:
            conf: dict = cls._load_config()

            if conf["type"] == RepositoryType.postgres.value:
                cls.repository_type = RepositoryType.postgres
                cls.url = cls.database_url(conf)
                db_engine = create_async_engine(
                    cls.url,
                    echo=True,
                )
                cls._session = async_sessionmaker(
                    bind=db_engine,
                    expire_on_commit=False,
                    class_=AsyncSession,
                )
                logger.debug("Используется подключение к PostgreSQL")
                return cls()
        except FileNotFoundError as e:
            logger.error("Файл конфигурации не найден: {}", e)
            raise NotFoundDatabaseConfig()
        logger.debug("Используется подключение к InMemory репозиторию")
        return cls()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self._session()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()

    @staticmethod
    def _load_config() -> dict:
        with open(settings.DB_CONF, "r") as file:
            conf = json.load(file)

        return conf

    @staticmethod
    def database_url(conf: dict) -> str:
        db_conf = PostgresConf(
            DB_SCHEME=conf.get("DB_SCHEME"),
            DB_USER=conf.get("DB_USER"),
            DB_PASS=conf.get("DB_PASS"),
            DB_HOST=conf.get("DB_HOST"),
            DB_NAME=conf.get("DB_NAME"),
            DB_PORT=conf.get("DB_PORT"),
        )

        return str(db_conf.url)
