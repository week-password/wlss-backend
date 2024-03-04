from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

from fastapi import status

from api.file.dtos import CreateFileResponse, GetFileResponse
from src.config import CONFIG
from src.file.models import File
from src.file.schemas import NewFile
from src.shared.minio import Minio


if TYPE_CHECKING:
    from pathlib import Path
    from uuid import UUID

    from fastapi import BackgroundTasks
    from sqlalchemy.ext.asyncio import AsyncSession

    from api.file.dtos import CreateFileRequest
    from src.account.models import Account


async def create_file(
    background_tasks: BackgroundTasks,
    request_data: CreateFileRequest,
    current_account: Account,  # noqa: ARG001
    session: AsyncSession,
) -> CreateFileResponse:
    new_file = NewFile.from_(request_data)
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
    return CreateFileResponse.model_validate(file, from_attributes=True)


async def get_file(
    background_tasks: BackgroundTasks,
    file_id: UUID,
    current_account: Account,  # noqa: ARG001
    tmp_dir: Path,
    session: AsyncSession,
) -> GetFileResponse:
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
    return GetFileResponse(
        file_path,
        status_code=status.HTTP_200_OK,
        media_type=file.mime_type.value,
    )
