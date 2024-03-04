from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dtos import CreateSessionRequest, CreateSessionResponse, RefreshTokensResponse
from api.shared.fields import IdField, UuidField
from src.account.models import Account
from src.auth import controllers
from src.auth.dependencies import get_account_from_access_token, get_account_from_refresh_token
from src.shared import swagger as shared_swagger
from src.shared.database import get_session


router = APIRouter(tags=["auth"])


@router.post(
    "/sessions",
    description="Sign In - create new auth session and generate access and refresh tokens for it.",
    responses={
        status.HTTP_201_CREATED: {"description": "Credentials are valid, new session and tokens are returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_201_CREATED,
    summary="Sign In - create tokens for new session.",
)
async def create_session(
    request_data: Annotated[CreateSessionRequest, Body()],
    session: AsyncSession = Depends(get_session),
) -> CreateSessionResponse:
    return await controllers.create_session(request_data, session)


@router.post(
    "/accounts/{account_id}/sessions/{session_id}/tokens",
    responses={
        status.HTTP_201_CREATED: {"description": "New access and refresh tokens are generated and returned."},
        status.HTTP_401_UNAUTHORIZED: shared_swagger.responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: shared_swagger.responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: shared_swagger.responses[status.HTTP_404_NOT_FOUND],
    },
    status_code=status.HTTP_201_CREATED,
    summary="Generate new access and refresh tokens for particular auth session",
)
async def refresh_tokens(
    account_id: Annotated[IdField, Path(example=42)],
    session_id: Annotated[UuidField, Path(example="b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")],
    current_account: Annotated[Account, Depends(get_account_from_refresh_token)],
    session: AsyncSession = Depends(get_session),
) -> RefreshTokensResponse:
    return await controllers.refresh_tokens(account_id, session_id, current_account, session)


@router.delete(
    "/accounts/{account_id}/sessions/{session_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Auth session is removed. User has been signed out."},
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
