from __future__ import annotations

import pytest
from wlss.account.types import AccountLogin
from wlss.shared.types import Id

from api.account.dtos import GetAccountsResponse


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts"})
async def test(f):
    result = await f.api.account.get_accounts(
        account_ids=[Id(1)],
        account_logins=[AccountLogin("john_smith")],
        token=f.access_token,
    )

    assert isinstance(result, GetAccountsResponse)
    assert result.model_dump() == {
        "accounts": [
            {"id": 1, "login": "john_doe"},
            {"id": 2, "login": "john_smith"},
        ],
    }
