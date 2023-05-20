"""MinIO related stuff."""

from __future__ import annotations

from typing import TYPE_CHECKING

import minio

from src.config import CONFIG
from src.shared import enum
from src.shared.types import UrlSchema


if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any, Final, Self


def get_minio() -> Iterator[Minio]:
    """Get minio client. FastAPI dependency for Minio client."""
    yield Minio(
        CONFIG.MINIO_SCHEMA,
        CONFIG.MINIO_HOST,
        CONFIG.MINIO_PORT,
        CONFIG.MINIO_ROOT_USER,
        CONFIG.MINIO_ROOT_PASSWORD,
    )


@enum.unique
@enum.types(str)
class Bucket(enum.Enum):
    """Enum for existing minio buckets."""

    ENTITY = "entity"


class Minio(minio.Minio):  # type: ignore[misc]
    """Minio client class. Used to extend minio.Minio functionality."""

    BUCKETS: Final[list[Bucket]] = list(Bucket)

    def __init__(
        self: Self,
        schema: UrlSchema,
        host: str,
        port: str,
        user: str,
        password: str,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize MinIO client which will be connected to MinIO.

        :param schema: URL schema for MinIO connection - "HTTP" or "HTTPS"
        :param host: host URL for MinIO connection, for example - "localhost"
        :param port: port for MinIO connection, for example - "9000"
        :param user: user name for MinIO connection, for example - "minioadmin"
        :param password: password for the user, for example - "minioadmin"
        :param args: other args for minio.Minio class
        :param kwargs: other kwargs for minio.Minio class
        """
        super().__init__(f"{host}:{port}", user, password, *args, secure=(schema is UrlSchema.HTTPS), **kwargs)
        self._create_missing_buckets()

    def _create_missing_buckets(self: Self) -> None:  # pragma: no cover
        """Create bucket if doesn't exist.."""
        for _, bucket_name in self.BUCKETS:
            if not self.bucket_exists(bucket_name):
                self.make_bucket(bucket_name)
