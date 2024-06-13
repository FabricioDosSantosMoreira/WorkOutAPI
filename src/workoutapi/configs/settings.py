from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):

    DB_URL: str = Field(default='postgresql+asyncpg://postgres:123456@localhost:5432/workout')


settings = Settings()