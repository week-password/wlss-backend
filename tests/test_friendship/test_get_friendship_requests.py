from __future__ import annotations

import dirty_equals
import pytest
from wlss.shared.types import Id

from api.friendship.dtos import GetFriendshipRequestsResponse
from api.friendship.enums import FriendshipRequestStatus
from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_three_accounts_and_three_friendship_requests",
})
async def test_get_friendship_requests_returns_correct_response(f):
    result = await f.api.friendship.get_friendship_requests(account_id=Id(1), token=f.access_token)

    assert isinstance(result, GetFriendshipRequestsResponse)
    assert result.model_dump() == {
        "requests": [
            {
                "id": dirty_equals.IsInt,
                "created_at": IsUtcDatetimeSerialized,
                "receiver_id": 2,
                "sender_id": 1,
                "status": FriendshipRequestStatus.PENDING,
            },
            {
                "id": dirty_equals.IsInt,
                "created_at": IsUtcDatetimeSerialized,
                "receiver_id": 1,
                "sender_id": 3,
                "status": FriendshipRequestStatus.PENDING,
            },
        ],
    }
