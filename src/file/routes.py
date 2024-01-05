"""File related endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_access_token
from src.auth.schemas import AccessTokenPayload
from src.file import controllers, schemas
from src.file.dependencies import get_new_file, get_tmp_dir
from src.shared import swagger as shared_swagger
from src.shared.database import get_session
from src.shared.minio import get_minio, Minio


router = APIRouter(tags=["file"])


@router.post(
    "/files",
    description="Upload new file.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "File uploaded, file info returned.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "47b3d7a9-d7d3-459a-aac1-155997775a0e",
                        "extension": "png",
                        "mime_type": "image/png",
                        "size": 2048,
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: shared_swagger.responses[status.HTTP_413_REQUEST_ENTITY_TOO_LARGE],
    },
    response_model=schemas.File,
    status_code=status.HTTP_201_CREATED,
    summary="Upload file.",
)
async def create_file(
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],
    new_file: Annotated[schemas.NewFile, Depends(get_new_file)],
    minio: Minio = Depends(get_minio),
    session: AsyncSession = Depends(get_session),
) -> schemas.File:
    """Create file."""
    return await controllers.create_file(access_token, new_file, minio, session)


@router.get(
    "/files/{file_id}",
    description="Get (download) uploaded file.",
    responses={
        status.HTTP_200_OK: {
            "description": "Uploaded file returned.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    summary="Get file.",
)
async def get_file(
    file_id: Annotated[UUID, Path(example="47b3d7a9-d7d3-459a-aac1-155997775a0e")],
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],
    tmp_dir: Annotated[Path, Depends(get_tmp_dir)],
    minio: Minio = Depends(get_minio),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Get file."""
    return await controllers.get_file(file_id, access_token, tmp_dir, minio, session)
