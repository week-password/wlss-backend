from __future__ import annotations

import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.shared.types import Id

from src.account.models import Account, PasswordHash
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
