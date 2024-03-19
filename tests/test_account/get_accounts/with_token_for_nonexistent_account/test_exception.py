from __future__ import annotations

import httpx
import pytest
from wlss.account.types import AccountLogin


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_with_nonexistent_account",
    "api": "api",
    "db": "db_with_one_account_and_one_session"})
async def test(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_accounts(account_logins=[AccountLogin("john_doe")], token=f.access_token)

    assert exc_info.value.response.status_code == 401
    assert exc_info.value.response.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }
