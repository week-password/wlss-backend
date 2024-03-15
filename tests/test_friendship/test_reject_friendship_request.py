from __future__ import annotations

from unittest.mock import patch

import dirty_equals
import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from api.friendship.dtos import RejectFriendshipRequestResponse
from api.friendship.enums import FriendshipRequestStatus
from src.friendship.models import FriendshipRequest
from src.shared.database import Base
from tests.utils.dirty_equals import IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_friendship_request_from_another_user",
})
async def test_reject_friendship_request_returns_correct_response(f):
    result = await f.api.friendship.reject_friendship_request(request_id=Id(1), token=f.access_token)

    assert isinstance(result, RejectFriendshipRequestResponse)
    assert result.model_dump() == {
        "id": dirty_equals.IsInt,
        "created_at": IsUtcDatetimeSerialized,
        "receiver_id": 1,
        "sender_id": 2,
        "status": FriendshipRequestStatus.REJECTED,
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_friendship_request_from_another_user",
})
async def test_reject_friendship_request_updates_objects_in_db_correctly(f):
    await f.api.friendship.reject_friendship_request(request_id=Id(1), token=f.access_token)

    with patch.object(Base, "__eq__", __eq__):
        friendship_requests = (await f.db.execute(select(FriendshipRequest))).scalars().all()
        assert friendship_requests == [
            FriendshipRequest(
                id=Id(1),
                created_at=IsUtcDatetime,
                sender_id=Id(2),
                receiver_id=Id(1),
                status=FriendshipRequestStatus.REJECTED,
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_one_friendship_request",
})
async def test_reject_friendship_request_with_friendship_request_from_another_user_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.friendship.reject_friendship_request(request_id=Id(1), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Reject friendship request.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
