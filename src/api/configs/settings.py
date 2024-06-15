from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_USER: str = Field(default="postgres")
    DB_PASS: str = Field(default="123456")
    DB_NAME: str = Field(default="workout")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: str = Field(default="5432")
    DB_URL: str = Field(default="empty")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # Constrói a URL de conexão com base nos valores das variáveis de ambiente '.env'
        self.DB_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_db_url(self) -> str:
        return self.DB_URL


# Cria uma instância da classe Settings para acessar as configurações
settings = Settings()
