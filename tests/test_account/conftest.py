from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.shared.types import Id

from api.shared.datetime import DATETIME_FORMAT
from src.account.models import Account, PasswordHash
from src.auth.models import Session
from src.config import CONFIG
from tests.utils import bcrypt as bcrypt_cached


@pytest.fixture
async def db_with_one_account(db_empty):
    session = db_empty

    account = Account(id=Id(1), email=AccountEmail("john.doe@mail.com"), login=AccountLogin("john_doe"))
    session.add(account)
    await session.flush()

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=Id(1), value=hash_value)
    session.add(password_hash)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_one_account_and_one_session(db_with_one_account):  # pylint: disable=redefined-outer-name
    session = db_with_one_account

    auth_session = Session(id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"), account_id=Id(1))
    session.add(auth_session)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_two_accounts(db_with_one_account_and_one_session):  # pylint: disable=redefined-outer-name
    session = db_with_one_account_and_one_session

    account = Account(id=Id(2), login=AccountLogin("john_smith"), email=AccountEmail("john.smith@mail.com"))
    session.add(account)
    await session.flush()

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=Id(2), value=hash_value)
    session.add(password_hash)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def access_token():
    payload = {
        "account_id": 1,
        "created_at": datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def access_token_with_nonexistent_account():
    payload = {
        "account_id": 42,
        "created_at": datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def access_token_expired():
    payload = {
        "account_id": 1,
        "created_at": (
            (
                datetime.now(tz=timezone.utc) - timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION + 1)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def access_token_incorrect():
    payload = {
        "account_id": 1,
        # missing "created_at" field
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
