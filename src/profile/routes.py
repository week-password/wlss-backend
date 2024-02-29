from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Account
from src.auth.dependencies import get_account_from_access_token
from src.profile import controllers, schemas
from src.shared import swagger as shared_swagger
from src.shared.database import get_session
from src.shared.fields import IdField


router = APIRouter(tags=["profile"])


@router.get(
    "/accounts/{account_id}/profile",
    description="Get Profile info related to particular user Account.",
    responses={
        status.HTTP_200_OK: {
            "description": "Profile info returned.",
            "content": {
                "application/json": {
                    "example": {
                        "account_id": 42,
                        "name": "John Doe",
                        "description": "Who da heck is John Doe?",
                        "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Profile,
    status_code=status.HTTP_200_OK,
    summary="Get Profile info.",
)
async def get_profile(
    account_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> schemas.Profile:
    return await controllers.get_profile(account_id, current_account, session)


@router.put(
    "/accounts/{account_id}/profile",
    description="Update Profile info.",
    responses={
        status.HTTP_200_OK: {
            "description": "Profile info is updated. Profile returned.",
            "content": {
                "application/json": {
                    "example": {
                        "account_id": 42,
                        "name": "John Doe",
                        "description": "Who da heck is John Doe?",
                        "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Profile,
    status_code=status.HTTP_200_OK,
    summary="Update Profile info.",
)
async def update_profile(
    account_id: Annotated[IdField, Path(example=42)],
    profile_update: Annotated[
        schemas.ProfileUpdate,
        Body(
            example={
                "name": "John Doe",
                "description": "Who da heck is John Doe?",
                "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
            },
        ),
    ],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> schemas.Profile:
    return await controllers.update_profile(account_id, profile_update, current_account, session)
