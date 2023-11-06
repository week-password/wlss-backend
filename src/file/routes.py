"""File related endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials

from src.auth import swagger as auth_swagger
from src.auth.security import get_token
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
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: auth_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.File,
    status_code=status.HTTP_201_CREATED,
    summary="Upload file.",
)
async def create_file(
    new_file: UploadFile,  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Create file."""


@router.get(
    "/files/{file_id}",
    description="Get uploaded file.",
    responses={
        status.HTTP_200_OK: {
            "description": "Uploaded file returned.",
        },
    },
    response_class=StreamingResponse,
    status_code=status.HTTP_200_OK,
    summary="Get file.",
)
def get_file(
    file_id: Annotated[UUID, Path(example="47b3d7a9-d7d3-459a-aac1-155997775a0e")],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get file."""
