"""Profile related endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import PositiveInt

from src.auth import swagger as auth_swagger
from src.auth.security import get_token
from src.profile import schemas
from src.shared import swagger as shared_swagger


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
                        "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: auth_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Profile,
    status_code=status.HTTP_200_OK,
    summary="Get Profile info.",
)
def get_profile(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get Profile info."""


@router.put(
    "/account/{account_id}/profile",
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
                        "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: auth_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Profile,
    status_code=status.HTTP_200_OK,
    summary="Update Profile info.",
)
def update_profile(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    profile_update: Annotated[  # noqa: ARG001
        schemas.ProfileUpdate,
        Body(
            example={
                "name": "John Doe",
                "description": "Who da heck is John Doe?",
                "avatar": "/files/0b928aaa-521f-47ec-8be5-396650e2a187",
            },
        ),
    ],
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Update profile info."""
