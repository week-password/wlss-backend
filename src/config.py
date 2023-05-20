"""Application configuration stuff."""

from typing import Final

from pydantic import BaseSettings

from src.shared.environment import load_environment
from src.shared.types import UrlSchema


load_environment()


class Config(BaseSettings):
    """Application config."""

    MINIO_HOST: str
    MINIO_PORT: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ROOT_USER: str
    MINIO_SCHEMA: UrlSchema

    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_USER: str

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic's special class to configure pydantic models."""

        allow_mutation = False  # app config should be immutable


CONFIG: Final = Config()
