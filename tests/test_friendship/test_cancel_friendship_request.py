from __future__ import annotations

import pytest
from sqlalchemy import select

from src.friendship.models import FriendshipRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_friendship_request"})
async def test_cancel_friendship_request_returns_204_with_correct_response(f):
    result = await f.client.delete("/friendships/requests/1", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 204
    assert result.content == b""


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_friendship_request"})
async def test_cancel_friendship_request_removes_objects_from_db_correctly(f):
    result = await f.client.delete(  # noqa: F841
        "/friendships/requests/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    friendship_requests = (await f.db.execute(select(FriendshipRequest))).scalars().all()
    assert friendship_requests == []


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts"})
async def test_cancel_friendship_request_with_nonexistent_request_returns_404_with_correct_response(f):
    result = await f.client.delete("/friendships/requests/42", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 404
    assert result.json() == {
        "resource": "Friendship request",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_friendship_request_from_another_user",
})
async def test_cancel_friendship_request_with_friendship_request_from_another_user_returns_403_with_correct_response(f):
    result = await f.client.delete("/friendships/requests/1", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 403
    assert result.json() == {
        "action": "Cancel friendship request.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
