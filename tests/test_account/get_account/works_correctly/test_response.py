from __future__ import annotations

import pytest
from wlss.shared.types import Id

from api.account.dtos import GetAccountResponse


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_one_account_and_one_session"})
async def test(f):
    result = await f.api.account.get_account(account_id=Id(1), token=f.access_token)

    assert isinstance(result, GetAccountResponse)
    assert result.model_dump() == {"id": 1, "login": "john_doe"}
