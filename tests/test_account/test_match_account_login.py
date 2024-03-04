from __future__ import annotations

import pytest

from api.account.dtos import MatchAccountLoginRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_match_account_login_returns_correct_response(f):
    result = await f.api.account.match_account_login(request_data=MatchAccountLoginRequest(login="john_doe"))

    assert result
