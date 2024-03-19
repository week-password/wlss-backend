from __future__ import annotations

import pytest
from wlss.shared.types import Id


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_two_sessions"})
async def test(f):
    result = await f.api.auth.delete_all_sessions(account_id=Id(1), token=f.access_token)

    assert result is None
