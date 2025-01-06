from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.shared.types import Id

from api.shared.datetime import DATETIME_FORMAT
from src.account.models import Account, PasswordHash
from src.config import CONFIG
from tests.utils import bcrypt as bcrypt_cached


@pytest.fixture
async def db_with_one_account(db_empty):
    session = db_empty

    account = Account(id=Id(1), email=AccountEmail("john.doe@mail.com"), login=AccountLogin("john_doe"))
    session.add(account)
    await session.flush()

    byte_password = base64.b64encode(hashlib.sha256(b"qwerty123").digest())
    hash_value = bcrypt_cached.hashpw(byte_password, salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=Id(1), value=hash_value)
    session.add(password_hash)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def redis_with_one_session(redis_empty):
    redis = redis_empty
    await redis.hset(
        "account_id:1",
        "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
        json.dumps({
            "account_id": 1,
            "created_at": datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT),
            "id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
        }),
    )
    return redis


@pytest.fixture
async def redis_with_two_sessions(redis_with_one_session):
    redis = redis_with_one_session
    await redis.hset(
        "account_id:1",
        "2ee55d6c-fe71-4ba0-9bbc-df074d365f60",
        json.dumps({
            "account_id": 1,
            "created_at": datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT),
            "id": "2ee55d6c-fe71-4ba0-9bbc-df074d365f60",
        })
    )
    return redis


@pytest.fixture
async def access_token():
    payload = {
        "account_id": 1,
        "created_at": datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def refresh_token():
    payload = {
        "account_id": 1,
        "created_at": datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def refresh_token_expired():
    payload = {
        "account_id": 1,
        "created_at": (
            (
                datetime.now(tz=timezone.utc) - timedelta(days=CONFIG.DAYS_BEFORE_REFRESH_TOKEN_EXPIRATION + 1)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")


@pytest.fixture
async def refresh_token_incorrect():
    payload = {
        "account_id": 1,
        # missing "created_at" field
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
