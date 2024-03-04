from __future__ import annotations

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.auth.models import Session


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_one_session"})
async def test_delete_all_sessions_returns_correct_response(f):
    result = await f.api.auth.delete_all_sessions(account_id=Id(1), token=f.access_token)

    assert result is None


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_two_sessions"})
async def test_delete_all_sessions_deletes_all_sessions_from_db_correctly(f):
    result = await f.api.auth.delete_all_sessions(account_id=Id(1), token=f.access_token)  # noqa: F841

    rows = (await f.db.execute(select(Session))).all()
    assert not rows


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_account_and_two_sessions",
})
async def test_delete_all_sessions_with_account_different_than_current_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.auth.delete_all_sessions(account_id=Id(42), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete all sessions",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
