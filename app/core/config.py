from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "PVIMP Backend"
    APP_NAME: str = "PVIMP Backend"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres123"
    DB_NAME: str = "pvimp_db"

    # مهم: فعلا دست نزن
    SECRET_KEY: str = "CHANGE_THIS_TO_A_RANDOM_LONG_SECRET_KEY"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()


def get_database_url() -> str:

    return (
        f"postgresql+psycopg2://{quote_plus(settings.DB_USER)}:"
        f"{quote_plus(settings.DB_PASSWORD)}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/"
        f"{settings.DB_NAME}"
    )
