from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import FileResponse

from src.config import CONFIG
from src.file import schemas
from src.file.models import File
from src.shared.minio import Minio


if TYPE_CHECKING:
    from pathlib import Path
    from uuid import UUID

    from fastapi import BackgroundTasks
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.account.models import Account


async def create_file(
    background_tasks: BackgroundTasks,
    new_file: schemas.NewFile,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> schemas.File:
    file = await File.create_file(session, new_file)
    minio = Minio(
        CONFIG.MINIO_SCHEMA,
        CONFIG.MINIO_HOST,
        CONFIG.MINIO_PORT,
        CONFIG.MINIO_ROOT_USER,
        CONFIG.MINIO_ROOT_PASSWORD,
    )
    minio.upload_file(file.id, new_file.tmp_file_path)

    background_tasks.add_task(shutil.rmtree, new_file.tmp_file_path.parent)
    return schemas.File(
        id=file.id,
        extension=file.extension,
        mime_type=file.mime_type,
        size=file.size,
    )


async def get_file(
    background_tasks: BackgroundTasks,
    file_id: UUID,
    current_account: Account,  # noqa: ARG001
    tmp_dir: Path,
    session: AsyncSession,
) -> FileResponse:
    file = await File.get(session, file_id)
    minio = Minio(
        CONFIG.MINIO_SCHEMA,
        CONFIG.MINIO_HOST,
        CONFIG.MINIO_PORT,
        CONFIG.MINIO_ROOT_USER,
        CONFIG.MINIO_ROOT_PASSWORD,
    )
    file_path = tmp_dir / file.name
    minio.download_file(file.id, file_path)

    background_tasks.add_task(shutil.rmtree, tmp_dir)
    return FileResponse(
        file_path,
        status_code=status.HTTP_200_OK,
        media_type=file.mime_type.value,
    )
