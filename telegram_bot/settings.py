import rtu_mirea_vuc_schedule_client
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

load_dotenv()


class DatabaseSettings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "chageme"
    db_password: str = "chageme"
    db_database: str = "app"
    db_pool_size: int = 20
    db_max_overflow: int = 5
    db_echo: bool = False

    @property
    def db_url(self):
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_database}"
        )

    @property
    def async_db_url(self):
        return self.db_url.replace("postgresql://", "postgresql+asyncpg://")


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6382
    redis_base: int | None = None
    redis_user: str | None = None
    redis_pass: str | None = None

    @property
    def redis_url(self) -> URL:
        path = "/"
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )


class ScheduleApiSettings(BaseSettings):
    schedule_api_base_url: str = "http://localhost:8000"

    @property
    def schedule_api_configuration(self):
        return rtu_mirea_vuc_schedule_client.Configuration(host=self.schedule_api_base_url)


class Settings(RedisSettings, DatabaseSettings, ScheduleApiSettings):
    log_level: str = "INFO"
    posthog_project_api_key: str | None = None
    token: str = ""

    model_config = SettingsConfigDict(
        env_prefix="TELEGRAM_BOT_",
        env_file_encoding="utf-8",
    )


settings = Settings()
