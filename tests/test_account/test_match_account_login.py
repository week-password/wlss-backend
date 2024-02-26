from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_match_account_login_returns_204_with_correct_response(f):
    result = await f.client.post(
        "/accounts/logins/match",
        json={"login": "john_doe"},
        headers={"Authorization": "Bearer token"},
    )

    assert result.status_code == 204
    assert result.content == b""
