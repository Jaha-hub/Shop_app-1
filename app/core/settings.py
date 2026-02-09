from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ACCESS_EXPIRES: int
    REFRESH_EXPIRES: int
    TOKEN_ALGORITHM: str
    TOKEN_SECRET_KEY: str

    ASYNC_DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()