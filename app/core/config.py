from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Enterprise Content Integration Hub"
    environment: str = "development"
    log_level: str = "INFO"

    database_url: str = (
        "postgresql+psycopg://integration:integration"
        "@postgres:5432/integration_hub"
    )

    redis_url: str = "redis://redis:6379/0"


settings = Settings()