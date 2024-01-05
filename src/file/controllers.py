"""Controllers functions for file entity."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import FileResponse

from src.file import schemas
from src.file.models import File


if TYPE_CHECKING:
    from uuid import UUID

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


async def get_file(
    file_id: UUID,
    access_token: AccessTokenPayload,  # noqa: ARG001
    tmp_dir: Path,
    minio: Minio,
    session: AsyncSession,
) -> FileResponse:
    """Get (download) file."""
    file = await File.get(session, file_id)
    file_path = Path(tmp_dir) / "file"
    minio.download_file(file.id, file_path)
    return FileResponse(file_path, status.HTTP_200_OK, media_type=str(file.mime_type))
