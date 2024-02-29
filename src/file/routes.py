from __future__ import annotations

import pathlib
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Path, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Account
from src.auth.dependencies import get_account_from_access_token
from src.file import controllers, schemas
from src.file.dependencies import get_new_file, get_tmp_dir
from src.shared import swagger as shared_swagger
from src.shared.database import get_session
from src.shared.fields import UuidField


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
    background_tasks: BackgroundTasks,
    new_file: Annotated[schemas.NewFile, Depends(get_new_file)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> schemas.File:
    return await controllers.create_file(background_tasks, new_file, current_account, session)


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
    background_tasks: BackgroundTasks,
    file_id: Annotated[UuidField, Path(example="47b3d7a9-d7d3-459a-aac1-155997775a0e")],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    tmp_dir: Annotated[pathlib.Path, Depends(get_tmp_dir)],
    session: AsyncSession = Depends(get_session),
) -> FileResponse:
    return await controllers.get_file(background_tasks, file_id, current_account, tmp_dir, session)
