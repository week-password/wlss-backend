"""Auth related endpoints."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, status
from pydantic import PositiveInt

from src.auth import schemas
from src.auth.dependencies import get_access_token, get_refresh_token
from src.shared import swagger as shared_swagger


router = APIRouter(tags=["auth"])


@router.post(
    "/sessions",
    description="Sign In - create new auth session and generate access and refresh tokens for it.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Credentials are valid, new session and tokens are returned.",
            "content": {
                "application/json": {
                    "example": {
                        "session": {
                            "id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
                            "account_id": 42,
                        },
                        "tokens": {
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
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=schemas.SessionWithTokens,
    status_code=status.HTTP_201_CREATED,
    summary="Sign In - create tokens for new session.",
)
async def create_session(
    credentials: Annotated[  # noqa: ARG001
        schemas.Credentials,
        Body(
            openapi_examples={
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
    """Create new auth session and generate tokens for particular account."""


@router.post(
    "/accounts/{account_id}/sessions/{session_id}/tokens",
    responses={
        status.HTTP_201_CREATED: {
            "description": "New access and refresh tokens are generated and returned.",
            "content": {
                "application/json": {
                    "example": {
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
    summary="Generate new access and refresh tokens for particular auth session",
)
async def refresh_tokens(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    session_id: Annotated[UUID, Path(example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")],  # noqa: ARG001
    refresh_token: Annotated[schemas.RefreshTokenPayload, Depends(get_refresh_token)],  # noqa: ARG001
) -> None:
    """Refresh tokens."""


@router.delete(
    "/accounts/{account_id}/sessions/{session_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Auth session is removed. User has been signed out.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Sign Out for particular auth session.",
)
async def delete_session(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    session_id: Annotated[UUID, Path(example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")],  # noqa: ARG001
    access_token: Annotated[schemas.AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Remove particular auth session."""


@router.delete(
    "/accounts/{account_id}/sessions",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "All auth sessions are removed. User has been signed out from all sessions.",
        },
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Sign Out from all sessions.",
)
async def delete_all_sessions(
    account_id: Annotated[PositiveInt, Path(example=42)],  # noqa: ARG001
    access_token: Annotated[schemas.AccessTokenPayload, Depends(get_access_token)],  # noqa: ARG001
) -> None:
    """Remove all auth sessions related to account."""
