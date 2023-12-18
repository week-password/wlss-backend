"""Controllers functions for file entity."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.file import schemas
from src.file.models import File


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.auth.schemas import AccessTokenPayload
    from src.shared.minio import Minio


async def create_file(
    access_token: AccessTokenPayload,  # noqa: ARG001
    new_file: schemas.NewFile,
    minio: Minio,
    session: AsyncSession,
) -> schemas.File:
    """Create (upload) a new file."""
    file = await File.create(session, new_file)
    minio.upload_file(file.id, new_file.file_path)
    return schemas.File.from_orm(file)
