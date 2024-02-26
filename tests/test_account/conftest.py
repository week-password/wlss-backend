from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
import pytest

from src.account.models import Account, PasswordHash
from src.auth.models import Session
from src.config import CONFIG
from src.shared.datetime import DATETIME_FORMAT
from tests.utils import bcrypt as bcrypt_cached


@pytest.fixture
async def db_with_one_account(db_empty):
    session = db_empty

    account = Account(id=1, email="john.doe@mail.com", login="john_doe")
    session.add(account)
    await session.flush()

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=account.id, value=hash_value)
    session.add(password_hash)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_one_account_and_one_session(db_with_one_account):  # pylint: disable=redefined-outer-name
    session = db_with_one_account

    auth_session = Session(id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"), account_id=1)
    session.add(auth_session)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def access_token():
    payload = {
        "account_id": 1,
        "expires_at": (
            (
                datetime.now(tz=timezone.utc) + timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def access_token_with_nonexistent_account():
    payload = {
        "account_id": 42,
        "expires_at": (
            (
                datetime.now(tz=timezone.utc) + timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def access_token_expired():
    payload = {
        "account_id": 1,
        "expires_at": (
            (
                datetime.now(tz=timezone.utc) - timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
