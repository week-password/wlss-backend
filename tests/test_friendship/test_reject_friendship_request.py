from __future__ import annotations

from unittest.mock import patch

import dirty_equals
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.friendship.enums import FriendshipRequestStatus
from src.friendship.models import FriendshipRequest
from src.shared.database import Base
from tests.utils.dirty_equals import IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_friendship_request"})
async def test_reject_friendship_request_returns_200_with_correct_response(f):
    result = await f.client.put(
        "/friendships/requests/1/rejected",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 200
    assert result.json() == {
        "id": dirty_equals.IsInt,
        "created_at": IsUtcDatetimeSerialized,
        "receiver_id": 2,
        "sender_id": 1,
        "status": "REJECTED",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_friendship_request"})
async def test_reject_friendship_request_updates_objects_in_db_correctly(f):
    result = await f.client.put(  # noqa: F841
        "/friendships/requests/1/rejected",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    with patch.object(Base, "__eq__", __eq__):
        friendship_requests = (await f.db.execute(select(FriendshipRequest))).scalars().all()
        assert friendship_requests == [
            FriendshipRequest(
                id=Id(1),
                created_at=IsUtcDatetime,
                sender_id=Id(1),
                receiver_id=Id(2),
                status=FriendshipRequestStatus.REJECTED,
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_friendship_request_from_another_user",
})
async def test_reject_friendship_request_with_friendship_request_from_another_user_returns_403_with_correct_response(f):
    result = await f.client.put(
        "/friendships/requests/1/rejected",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Reject friendship request.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
