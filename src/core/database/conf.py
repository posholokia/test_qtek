from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


load_dotenv()


class PostgresConf(BaseSettings):
    DB_SCHEME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int

    @property
    def url(self):
        return PostgresDsn.build(
            scheme=self.DB_SCHEME,
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
