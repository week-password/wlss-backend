from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.exceptions import AccountNotFoundError
from src.account.models import Account
from src.auth.exceptions import InvalidCredentialsError, SessionNotFoundError, TokenExpiredError
from src.auth.schemas import AccessTokenPayload, RefreshTokenPayload
from src.config import CONFIG
from src.shared.database import get_session


async def get_account_from_access_token(
    authorization: Annotated[
        HTTPAuthorizationCredentials,
        Depends(
            HTTPBearer(
                scheme_name="Access token",
                description="Short-living token needed to authenticate the request.",
            ),
        ),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Account:
    try:
        payload = AccessTokenPayload.decode(authorization.credentials)
    except jwt.DecodeError:
        # pylint: disable-next=raise-missing-from
        raise InvalidCredentialsError()  # noqa: TRY200, B904
    except ValidationError as e:
        raise RequestValidationError(e.errors()) from None

    datetime_now = datetime.now(tz=timezone.utc)
    if datetime_now > payload.created_at.value + timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION):
        raise TokenExpiredError()

    try:  # pylint: disable=too-many-try-statements
        current_account = await Account.get(session, payload.account_id)
        await current_account.get_session(session, payload.session_id)
    except (SessionNotFoundError, AccountNotFoundError):
        # pylint: disable-next=raise-missing-from
        raise InvalidCredentialsError()  # noqa: B904,TRY200

    return current_account


async def get_account_from_refresh_token(
    authorization: Annotated[
        HTTPAuthorizationCredentials,
        Depends(
            HTTPBearer(
                scheme_name="Refresh token",
                description="Long-living token needed to refresh expired tokens.",
            ),
        ),
    ],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Account:
    try:
        payload = RefreshTokenPayload.decode(authorization.credentials)
    except jwt.DecodeError:
        # pylint: disable-next=raise-missing-from
        raise InvalidCredentialsError()  # noqa: TRY200, B904
    except ValidationError as e:
        raise RequestValidationError(e.errors()) from None

    datetime_now = datetime.now(tz=timezone.utc)
    if datetime_now > payload.created_at.value + timedelta(days=CONFIG.DAYS_BEFORE_REFRESH_TOKEN_EXPIRATION):
        raise TokenExpiredError()

    try:  # pylint: disable=too-many-try-statements
        current_account = await Account.get(session, payload.account_id)
        await current_account.get_session(session, payload.session_id)
    except (SessionNotFoundError, AccountNotFoundError):
        # pylint: disable-next=raise-missing-from
        raise InvalidCredentialsError()  # noqa: B904,TRY200

    return current_account
