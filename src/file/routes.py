"""File related endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status, UploadFile
from fastapi.responses import FileResponse

from src.auth.dependencies import get_access_token
from src.auth.schemas import AccessTokenPayload
from src.file import schemas
from src.shared import swagger as shared_swagger


router = APIRouter(tags=["file"])


@router.post(
    "/files",
    description="Upload new file.",
    responses={
        status.HTTP_200_OK: {
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
    },
    response_model=schemas.File,
    status_code=status.HTTP_201_CREATED,
    summary="Upload file.",
)
async def create_file(
    new_file: UploadFile,  # noqa: ARG001
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Create file."""


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
    file_id: Annotated[UUID, Path(example="47b3d7a9-d7d3-459a-aac1-155997775a0e")],  # noqa: ARG001
    access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Get file."""
