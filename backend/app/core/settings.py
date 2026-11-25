from typing import Annotated, Literal

from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Адрес базы в стандартном виде: postgresql://user:password@host:port/db.
    # Так его выдаёт сервер, и так же его читает entrypoint.prod.sh.
    DATABASE_URL: str

    ENABLE_DOCS: bool
    CORS_ALLOWED_ORIGINS: list[str]
    FRONTEND_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_LEEWAY_SECONDS: int
    EMAIL_TOKEN_TTL_MINUTES: int

    REFRESH_TOKEN_EXPIRE_DAYS: int
    REFRESH_COOKIE_NAME: str
    REFRESH_COOKIE_PATH: str
    COOKIE_DOMAIN: str
    SECURE_COOKIES: bool
    SAMESITE_COOKIES: Annotated[
        Literal["lax", "strict", "none"], BeforeValidator(str.lower)
    ]

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str
    SMTP_USE_TLS: bool

    RABBITMQ_URL: str

    # Адрес для SQLAlchemy и alembic: асинхронному драйверу нужна схема
    # postgresql+asyncpg://, поэтому меняем её здесь, а не в .env.
    # Возвращаем объект URL, а не строку: str(url) прячет пароль.
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> URL:
        return make_url(self.DATABASE_URL).set(drivername="postgresql+asyncpg")


settings = Settings()  # type: ignore
