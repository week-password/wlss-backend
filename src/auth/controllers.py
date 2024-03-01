from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.auth import schemas
from src.auth.dtos import CreateSessionResponse, RefreshTokensResponse
from src.auth.exceptions import (
    CannotDeleteAllSessionsError,
    CannotDeleteSessionError,
    CannotRefreshTokensError,
)
from src.auth.schemas import Credentials


if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.shared.types import Id

    from src.auth.dtos import CreateSessionRequest


async def create_session(request_data: CreateSessionRequest, session: AsyncSession) -> CreateSessionResponse:
    credentials = Credentials.from_(request_data)
    account = await Account.get_by_credentials(session, credentials)
    auth_session = await account.create_session(session)
    access_token = schemas.AccessTokenPayload(account_id=auth_session.account_id, session_id=auth_session.id)
    refresh_token = schemas.RefreshTokenPayload(account_id=auth_session.account_id, session_id=auth_session.id)
    return CreateSessionResponse.model_validate(
        {
            "session": auth_session,
            "tokens": {
                "access_token": access_token.encode(),
                "refresh_token": refresh_token.encode(),
            },
        },
        from_attributes=True,
    )


async def refresh_tokens(
    account_id: Id,
    session_id: UUID,
    current_account: Account,
    session: AsyncSession,
) -> RefreshTokensResponse:
    if account_id != current_account.id:
        raise CannotRefreshTokensError()

    auth_session = await current_account.get_session(session, session_id)
    access_token = schemas.AccessTokenPayload(account_id=auth_session.account_id, session_id=auth_session.id)
    refresh_token = schemas.RefreshTokenPayload(account_id=auth_session.account_id, session_id=auth_session.id)
    return RefreshTokensResponse(access_token=access_token.encode(), refresh_token=refresh_token.encode())


async def delete_session(
    account_id: Id,
    session_id: UUID,
    current_account: Account,
    session: AsyncSession,
) -> None:
    if (
        not await current_account.has_session(session, session_id)
        or not account_id == current_account.id
    ):
        raise CannotDeleteSessionError()

    auth_session = await current_account.get_session(session, session_id)
    await auth_session.delete(session)


async def delete_all_sessions(
    account_id: Id,
    current_account: Account,
    session: AsyncSession,
) -> None:
    if account_id != current_account.id:
        raise CannotDeleteAllSessionsError()
    await current_account.delete_all_sessions(session)
