from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from wlss.shared.types import UtcDatetime

from api.auth.dtos import CreateSessionResponse, RefreshTokensResponse
from src.account.models import Account
from src.auth import schemas
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

    from api.auth.dtos import CreateSessionRequest
    from src.auth.storage import SessionStorage


async def create_session(
    request_data: CreateSessionRequest,
    session_storage: SessionStorage,
    session: AsyncSession,
) -> CreateSessionResponse:
    credentials = Credentials.from_(request_data)
    account = await Account.get_by_credentials(session, credentials)
    auth_session = await session_storage.create_session(account.id)
    access_token = schemas.AccessTokenPayload(
        account_id=auth_session.account_id,
        created_at=UtcDatetime(datetime.now(tz=timezone.utc)),
        session_id=auth_session.id,
    )
    refresh_token = schemas.RefreshTokenPayload(
        account_id=auth_session.account_id,
        created_at=UtcDatetime(datetime.now(tz=timezone.utc)),
        session_id=auth_session.id,
    )
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
    session_storage: SessionStorage,
    session: AsyncSession,
) -> RefreshTokensResponse:
    if account_id != current_account.id:
        raise CannotRefreshTokensError()

    auth_session = await session_storage.get_session(account_id, session_id)
    access_token = schemas.AccessTokenPayload(
        account_id=auth_session.account_id,
        created_at=UtcDatetime(datetime.now(tz=timezone.utc)),
        session_id=auth_session.id,
    )
    refresh_token = schemas.RefreshTokenPayload(
        account_id=auth_session.account_id,
        created_at=UtcDatetime(datetime.now(tz=timezone.utc)),
        session_id=auth_session.id,
    )
    return RefreshTokensResponse(access_token=access_token.encode(), refresh_token=refresh_token.encode())


async def delete_session(
    account_id: Id,
    session_id: UUID,
    current_account: Account,
    session_storage: SessionStorage,
) -> None:
    if (
        not (await session_storage.has_session(account_id, session_id))
        or not account_id == current_account.id
    ):
        raise CannotDeleteSessionError()

    await session_storage.delete_session(account_id, session_id)


async def delete_all_sessions(
    account_id: Id,
    current_account: Account,
    session_storage: SessionStorage,
) -> None:
    if account_id != current_account.id:
        raise CannotDeleteAllSessionsError()
    await session_storage.delete_all_sessions(account_id)
