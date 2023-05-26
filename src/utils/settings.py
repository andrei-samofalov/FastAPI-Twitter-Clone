from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = './media'

TESTING = False
USE_SENTRY = False


class Settings(BaseSettings):
    real_db: str = Field(..., env="REAL_DATABASE_URL")
    dev_db: str = Field(..., env="DEV_DATABASE_URL")
    test_db: str = Field(..., env="TEST_DATABASE_URL")
    sentry_dsn: str = Field(..., env="DSN")
    debug: bool = Field(..., env="DEBUG")

    class Config:  # noqa
        env_prefix = ""
        case_sensitive = False
        # env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


def get_settings():
    """
    Возвращает объект настроек pydantic
    :rtype: Settings
    """
    return Settings()


def get_db_url():
    """
    Возвращает ссылку на базу данных в зависимости от флага DEBUG
    :rtype: str
    """
    s = get_settings()
    return s.dev_db if s.debug else s.real_db
