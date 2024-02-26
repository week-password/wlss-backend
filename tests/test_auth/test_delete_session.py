from __future__ import annotations

import pytest
from sqlalchemy import select

from src.auth.models import Session


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "access_token": "access_token",
    "db": "db_with_one_account_and_one_session",
})
async def test_delete_session_returns_204_with_correct_response(f):
    result = await f.client.delete(
        "/accounts/1/sessions/b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 204
    assert result.content == b""


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "access_token": "access_token",
    "db": "db_with_one_account_and_one_session",
})
async def test_delete_session_deletes_session_from_db_correctly(f):
    result = await f.client.delete(  # noqa: F841
        "/accounts/1/sessions/b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    rows = (await f.db.execute(select(Session))).all()
    assert not rows


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "access_token": "access_token", "db": "db_with_one_account_and_one_session"})
async def test_delete_session_with_different_session_ids_in_url_path_and_token_returns_403_with_correct_response(f):
    result = await f.client.delete(
        "/accounts/1/sessions/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Delete session",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_delete_session_with_invalid_token_returns_401_with_correct_response(f):
    result = await f.client.delete(
        "/accounts/1/sessions/b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
        headers={"Authorization": "Bearer invalid token"},
    )

    assert result.status_code == 401
    assert result.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }
