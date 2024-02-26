from __future__ import annotations

import pytest
from sqlalchemy import select

from src.file.models import File
from src.wish.models import Wish


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_wish"})
async def test_delete_wish_returns_204_with_correct_response(f):
    result = await f.client.delete(
        "/accounts/1/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 204
    assert result.content == b""


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_wish"})
async def test_delete_wish_deletes_objects_from_db_correctly(f):
    result = await f.client.delete(  # noqa: F841
        "/accounts/1/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    wishes = (await f.db.execute(select(Wish))).all()
    assert wishes == []
    files = (await f.db.execute(select(File))).all()
    assert files == []


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts_and_one_wish"})
async def test_delete_wish_with_another_account_returns_403_with_correct_response(f):
    result = await f.client.delete(
        "/accounts/2/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Delete wish.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_wish_without_avatar"})
async def test_delete_wish_without_avatar_returns_204_with_correct_response(f):
    result = await f.client.delete(
        "/accounts/1/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 204
    assert result.content == b""
