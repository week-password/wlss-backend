from __future__ import annotations

import pytest
from sqlalchemy import select

from src.friendship.models import Friendship


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_friendships"})
async def test_delete_friendships_returns_200_with_correct_response(f):
    result = await f.client.delete("/accounts/1/friendships/2", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 204
    assert result.content == b""


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_friendships"})
async def test_delete_friendships_deletes_objects_from_db_correctly(f):
    result = await f.client.delete(  # noqa: F841
        "/accounts/1/friendships/2",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    friendships = (await f.db.execute(select(Friendship))).scalars().all()
    assert friendships == []


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_friendships"})
async def test_delete_friendships_with_another_users_friendship_returns_200_with_correct_response(f):
    result = await f.client.delete("/accounts/2/friendships/2", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 403
    assert result.json() == {
        "action": "Delete friendship.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
