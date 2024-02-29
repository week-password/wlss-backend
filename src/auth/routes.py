from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import Account
from src.auth import controllers, schemas
from src.auth.dependencies import get_account_from_access_token, get_account_from_refresh_token
from src.shared import swagger as shared_swagger
from src.shared.database import get_session
from src.shared.fields import IdField, UuidField


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
    credentials: Annotated[
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
    session: AsyncSession = Depends(get_session),
) -> schemas.SessionWithTokens:
    return await controllers.create_session(credentials, session)


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
    account_id: Annotated[IdField, Path(example=42)],
    session_id: Annotated[UuidField, Path(example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")],
    current_account: Annotated[Account, Depends(get_account_from_refresh_token)],
    session: AsyncSession = Depends(get_session),
) -> schemas.Tokens:
    return await controllers.refresh_tokens(account_id, session_id, current_account, session)


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
    account_id: Annotated[IdField, Path(example=42)],
    session_id: Annotated[UuidField, Path(example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> None:
    return await controllers.delete_session(account_id, session_id, current_account, session)


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
    account_id: Annotated[IdField, Path(example=42)],
    current_account: Annotated[Account, Depends(get_account_from_access_token)],
    session: AsyncSession = Depends(get_session),
) -> None:
    return await controllers.delete_all_sessions(account_id, current_account, session)
