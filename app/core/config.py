from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    postgres_user: str = "app"
    postgres_password: str = "app"
    postgres_db: str = "app"
    postgres_host: str = "localhost"
    postgres_port: int = 55432

    default_admin_user: str = "admin"
    default_admin_password: str = "admin"

    app_name: str = "FastAPI CRUD"
    debug: bool = False

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
