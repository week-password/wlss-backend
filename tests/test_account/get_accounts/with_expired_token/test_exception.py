from __future__ import annotations

import httpx
import pytest
from wlss.account.types import AccountLogin


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token_expired", "api": "api"})
async def test(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_accounts(
            account_logins=[AccountLogin("john_doe")],
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Token validation",
        "description": "Token expired.",
        "details": "Provided token is expired.",
    }
