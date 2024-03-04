from __future__ import annotations

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.file.models import File
from src.wish.models import Wish


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_wish"})
async def test_delete_wish_returns_correct_response(f):
    result = await f.api.wish.delete_wish(account_id=Id(1), wish_id=Id(1), token=f.access_token)

    assert result is None


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_wish"})
async def test_delete_wish_deletes_objects_from_db_correctly(f):
    result = await f.api.wish.delete_wish(account_id=Id(1), wish_id=Id(1), token=f.access_token)  # noqa: F841

    wishes = (await f.db.execute(select(Wish))).all()
    assert wishes == []
    files = (await f.db.execute(select(File))).all()
    assert files == []


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts_and_one_wish"})
async def test_delete_wish_with_another_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.delete_wish(account_id=Id(2), wish_id=Id(1), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete wish.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_one_wish_without_avatar"})
async def test_delete_wish_without_avatar_returns_204_with_correct_response(f):
    result = await f.api.wish.delete_wish(account_id=Id(1), wish_id=Id(1), token=f.access_token)

    assert result is None
