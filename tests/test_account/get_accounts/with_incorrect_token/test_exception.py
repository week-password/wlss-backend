from __future__ import annotations

import httpx
import pytest
from wlss.account.types import AccountLogin


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token_incorrect", "api": "api"})
async def test(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_accounts(
            account_logins=[AccountLogin("john_doe")],
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 422
    assert exc_info.value.response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["created_at"],
                "msg": "Field required",
                "input": {
                    "account_id": 1,
                    "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
                },
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ],
    }
