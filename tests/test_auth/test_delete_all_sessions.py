from __future__ import annotations

import pytest
from sqlalchemy import select

from src.auth.models import Session


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "access_token": "access_token",
    "db": "db_with_one_account_and_two_sessions",
})
async def test_delete_all_sessions_returns_204_with_correct_response(f):
    result = await f.client.delete("/accounts/1/sessions", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 204
    assert result.content == b""


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "access_token": "access_token",
    "db": "db_with_one_account_and_two_sessions",
})
async def test_delete_all_sessions_deletes_all_sessions_from_db_correctly(f):
    result = await f.client.delete(  # noqa: F841
        "/accounts/1/sessions",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    rows = (await f.db.execute(select(Session))).all()
    assert not rows


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "access_token": "access_token",
    "db": "db_with_one_account_and_two_sessions",
})
async def test_delete_all_sessions_with_account_different_than_current_account_returns_403_with_correct_response(f):
    result = await f.client.delete("/accounts/42/sessions", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 403
    assert result.json() == {
        "action": "Delete all sessions",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
