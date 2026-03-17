from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    api_open_ia: str = Field(alias="API_OPEN_IA")
    base_name: str = Field(alias="BASE_NAME")
    base_user: str = Field(alias="BASE_USER")
    base_password: str = Field(alias="BASE_PASSWORD")
    base_host: str = Field(alias="BASE_HOST")
    base_port: int = Field(alias="BASE_PORT")
    model_ia: str = Field(alias="MODEL_IA")
    auth_secret_key: str = Field(default="change-this-auth-secret", alias="AUTH_SECRET_KEY")
    auth_token_ttl_minutes: int = Field(default=1440, alias="AUTH_TOKEN_TTL_MINUTES")
    login_rate_limit_per_minute: int = Field(default=2, alias="LOGIN_RATE_LIMIT_PER_MINUTE")
    login_min_interval_seconds: int = Field(default=3, alias="LOGIN_MIN_INTERVAL_SECONDS")
    recaptcha_secret_key: str | None = Field(default=None, alias="RECAPTCHA_SECRET_KEY")
    app_name: str = "Titulos UPAO API"
    session_ttl_hours: int = 24
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.base_user}:{self.base_password}"
            f"@{self.base_host}:{self.base_port}/{self.base_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
