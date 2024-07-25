import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG")
    DB_CONF: str = os.getenv("DB_CONF")


settings = Settings()
