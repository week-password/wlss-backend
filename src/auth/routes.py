"""Auth related endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import PositiveInt

from src.auth import schemas
from src.auth.security import get_token
from src.shared import swagger as shared_swagger


router = APIRouter(tags=["auth"])


@router.post(
    "/accounts",
    description="Sign Up - create a new account with profile.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "New account and profile are created.",
            "content": {
                "application/json": {
                    "example": {
                        "account": {
                            "id": 42,
                            "email": "john.doe@mail.com",
                            "login": "john_doe",
                            "created_at": "2023-06-17T11:47:02.823Z",
                        },
                        "profile": {
                            "account_id": 42,
                            "avatar": None,
                            "description": "Who da heck is John Doe?",
                            "name": "John Doe",
                        },
                    },
                },
            },
        },
    },
    response_model=schemas.AccountWithProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Sign Up - create a new account.",
)
async def create_account(
    new_account: Annotated[  # noqa: ARG001
        schemas.NewAccountWithProfile,
        Body(
            example={
                "account": {
                    "email": "john.doe@mail.com",
                    "login": "john_doe",
                    "password": "qwerty123",
                },
                "profile": {
                    "name": "John Doe",
                    "description": "Who da heck is John Doe?",
                },
            },
        ),
    ],
) -> None:
    """Create a new account with profile."""


@router.post(
    "/accounts/{account_id}/tokens",
    description="Sign In - exchange account credentials to Access and Refresh tokens.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Credentials are valid, fresh tokens for new device are created.",
            "content": {
                "application/json": {
                    "example": {
                        "device_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
                        "access_token": (
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6N"
                            "DJ9.YKVpm2zdxup0_ts81Ft4USo-AUMKXBCTfgXtNFbRLlg"
                        ),
                        "refresh_token": (
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MiwiZGV2aWNlX2lkIj"
                            "oxOCwiZXhwIjoxNjg3MjU2MTMxfQ.GgXVGPV1aE2GjyRWN_IrHaEkZwY_x0gs25lJKtgspX0"
                        ),
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Tokens,
    status_code=status.HTTP_201_CREATED,
    summary="Sign In - create tokens for new device.",
)
async def create_tokens(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    credentials: Annotated[  # noqa: ARG001
        schemas.Credentials,
        Body(
            examples={
                "With login": {
                    "description": "Sign In via login and password.",
                    "value": {
                        "login": "john_doe",
                        "password": "qwerty123",
                    },
                },
                "With email": {
                    "description": "Sign In via email and password.",
                    "value": {
                        "email": "john.doe@mail.com",
                        "password": "qwerty123",
                    },
                },
                "Invalid - no login, no email": {
                    "description": "Invalid request - email or login is required.",
                    "value": {
                        "password": "qwerty123",
                    },
                },
                "Invalid - both login and email": {
                    "description": "Invalid request - you can not use login and email together.",
                    "value": {
                        "login": "john_doe",
                        "email": "john.doe@mail.com",
                        "password": "qwerty123",
                    },
                },
            },
        ),
    ],
) -> None:
    """Create new tokens for the account."""


@router.put(
    "/accounts/{account_id}/tokens/{device_id}/refresh",
    responses={
        status.HTTP_200_OK: {
            "description": "Exchange refresh token to the new Access and Refresh tokens.",
            "content": {
                "application/json": {
                    "example": {
                        "device_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
                        "access_token": (
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6N"
                            "DJ9.YKVpm2zdxup0_ts81Ft4USo-AUMKXBCTfgXtNFbRLlg"
                        ),
                        "refresh_token": (
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MiwiZGV2aWNlX2lkIj"
                            "oxOCwiZXhwIjoxNjg3MjU2MTMxfQ.GgXVGPV1aE2GjyRWN_IrHaEkZwY_x0gs25lJKtgspX0"
                        ),
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.Tokens,
    status_code=status.HTTP_200_OK,
    summary="Refresh tokens for one device.",
)
async def refresh_tokens(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    device_id: Annotated[UUID, Path(example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")],  # noqa: ARG001
    tokens: Annotated[  # noqa: ARG001
        schemas.RefreshToken,
        Body(
            example={
                "refresh_token": (
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MiwiZGV2aWNlX2lkIj"
                    "oxOCwiZXhwIjoxNjg3MjU2MTMxfQ.GgXVGPV1aE2GjyRWN_IrHaEkZwY_x0gs25lJKtgspX0"
                ),
            },
        ),
    ],
) -> None:
    """Refresh tokens."""


@router.delete(
    "/accounts/{account_id}/tokens/{device_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "All tokens for particular device are removed. User has been signed out from this device.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Sign Out from one device.",
)
async def remove_device_tokens(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    device_id: Annotated[UUID, Path(example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Remove tokens for particular device."""


@router.delete(
    "/accounts/{account_id}/tokens",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "All account tokens are removed. User has been signed out from all devices.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Sign Out from all devices.",
)
async def remove_all_tokens(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Remove tokens for all devices related to account."""
