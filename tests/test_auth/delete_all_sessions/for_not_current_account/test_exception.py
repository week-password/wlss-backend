from __future__ import annotations

import httpx
import pytest
from wlss.shared.types import Id


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_account_and_two_sessions",
})
async def test(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.auth.delete_all_sessions(account_id=Id(42), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete all sessions",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
