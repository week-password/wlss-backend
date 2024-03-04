from __future__ import annotations

import pathlib
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.file.dtos import CreateFileRequest, CreateFileResponse, GetFileResponse
from api.shared.fields import UuidField
from src.account.models import Account
from src.auth.dependencies import get_account_from_access_token
from src.file import controllers
from src.file.dependencies import get_new_file, get_tmp_dir
from src.shared import swagger as shared_swagger
from src.shared.database import get_session


router = APIRouter(tags=["file"])


@router.post(
    "/files",
    description="Upload new file.",
    responses={
        status.HTTP_201_CREATED: {"description": "File uploaded, file info returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
    },
    status_code=status.HTTP_201_CREATED,
    summary="Upload file.",
)
async def create_file(
    background_tasks: BackgroundTasks,
    request_data: Annotated[CreateFileRequest, Depends(get_new_file)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> CreateFileResponse:
    return await controllers.create_file(background_tasks, request_data, current_account, session)


@router.get(
    "/files/{file_id}",
    description="Get (download) uploaded file.",
    responses={
        status.HTTP_200_OK: {"description": "Uploaded file returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_200_OK,
    summary="Get file.",
)
async def get_file(
    background_tasks: BackgroundTasks,
    file_id: Annotated[UuidField, Path(example="47b3d7a9-d7d3-459a-aac1-155997775a0e")],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    tmp_dir: Annotated[pathlib.Path, Depends(get_tmp_dir)],
    session: AsyncSession = Depends(get_session),
) -> GetFileResponse:
    return await controllers.get_file(background_tasks, file_id, current_account, tmp_dir, session)
