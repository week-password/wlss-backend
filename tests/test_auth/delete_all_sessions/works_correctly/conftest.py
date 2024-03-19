from __future__ import annotations

from datetime import datetime, timezone
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
async def db_with_one_account_and_two_sessions(db_empty):
    session = db_empty

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    session.add_all([
        Account(id=Id(1), email=AccountEmail("john.doe@mail.com"), login=AccountLogin("john_doe")),
        PasswordHash(account_id=Id(1), value=hash_value),
        Session(account_id=Id(1), id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec")),
        Session(account_id=Id(1), id=UUID("2ee55d6c-fe71-4ba0-9bbc-df074d365f60")),
    ])
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
