from __future__ import annotations

import pytest

from src.account.models import Account


@pytest.fixture
async def db_with_one_account(db_empty):
    session = db_empty
    account = Account(email="john.doe@mail.com", login="john_doe")
    session.add(account)
    await session.commit()
    return session
