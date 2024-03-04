from __future__ import annotations

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.friendship.models import Friendship


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_friendships"})
async def test_delete_friendships_returns_correct_response(f):
    result = await f.api.friendship.delete_friendships(
        account_id=Id(1),
        friend_id=Id(2),
        token=f.access_token,
    )

    assert result is None


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_friendships"})
async def test_delete_friendships_deletes_objects_from_db_correctly(f):
    result = await f.api.friendship.delete_friendships(  # noqa: F841
        account_id=Id(1),
        friend_id=Id(2),
        token=f.access_token,
    )

    friendships = (await f.db.execute(select(Friendship))).scalars().all()
    assert friendships == []


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_friendships"})
async def test_delete_friendships_with_another_users_friendship_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.friendship.delete_friendships(
            account_id=Id(2),
            friend_id=Id(2),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete friendship.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
