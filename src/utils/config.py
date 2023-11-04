from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 0
    SQLALCHEMY_DATABASE_URL: str = ""
    PAGE_SIZE: int = 0

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()