from __future__ import annotations

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.friendship.models import FriendshipRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_friendship_request"})
async def test_cancel_friendship_request_returns_correct_response(f):
    result = await f.api.friendship.cancel_friendship_request(request_id=Id(1), token=f.access_token)

    assert result is None


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_friendship_request"})
async def test_cancel_friendship_request_removes_objects_from_db_correctly(f):
    result = await f.api.friendship.cancel_friendship_request(request_id=Id(1), token=f.access_token)  # noqa: F841

    friendship_requests = (await f.db.execute(select(FriendshipRequest))).scalars().all()
    assert friendship_requests == []


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts"})
async def test_cancel_friendship_request_with_nonexistent_request_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.friendship.cancel_friendship_request(request_id=Id(42), token=f.access_token)

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "Friendship request",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_friendship_request_from_another_user",
})
async def test_cancel_friendship_request_with_friendship_request_from_another_user_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.friendship.cancel_friendship_request(request_id=Id(1), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Cancel friendship request.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
