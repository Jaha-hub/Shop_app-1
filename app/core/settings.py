from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    ACCESS_EXPIRES: int
    REFRESH_EXPIRES: int
    TOKEN_ALGORITHM: str
    TOKEN_SECRET_KEY: str

    ASYNC_DATABASE_URL: str

    DATABASE_URL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    BACKEND_URL: str



    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()
