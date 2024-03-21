import os
from typing import ClassVar

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()  # take environment variables from .env.
ENVIRONMENT = os.environ.get("ENVIRONMENT")


class Settings(BaseSettings):
    ENVIRONMENT: str = ENVIRONMENT

    PROJECT_NAME: str = "Loans API Service"
    DESCRIPTION: str = "Microservice to manage costumers loans and payments"

    DEFAULT_TIMEZONE: str = "America/Mexico_City"

    VERSION: str = "1.0.0"
    API_V1: str = "v1"
    DEFAULT_PAGE_SIZE: int = 30

    # Database Settings
    # ----------------------------------------------------------------------------------
    POSTGRESQL_URL: PostgresDsn

    # API Settings
    # ----------------------------------------------------------------------------------
    CORS_ALLOWED_ORIGINS: ClassVar[list[str]] = ["*"]

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=True)
