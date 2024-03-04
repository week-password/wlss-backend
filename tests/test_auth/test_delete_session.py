from __future__ import annotations

from uuid import UUID

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.auth.models import Session


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_one_session"})
async def test_delete_session_returns_204_with_correct_response(f):
    result = await f.api.auth.delete_session(
        account_id=Id(1),
        session_id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"),
        token=f.access_token,
    )

    assert result is None


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_one_session"})
async def test_delete_session_deletes_session_from_db_correctly(f):
    result = await f.api.auth.delete_session(  # noqa: F841
        account_id=Id(1),
        session_id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"),
        token=f.access_token,
    )

    rows = (await f.db.execute(select(Session))).all()
    assert not rows


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_one_session"})
async def test_delete_session_with_different_session_ids_in_url_path_and_token_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.auth.delete_session(
            account_id=Id(1),
            session_id=UUID("00000000-0000-0000-0000-000000000000"),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete session",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_delete_session_with_invalid_token_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.auth.delete_session(
            account_id=Id(1),
            session_id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"),
            token="invalid token",  # noqa: S106
        )

    assert exc_info.value.response.status_code == 401
    assert exc_info.value.response.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }
