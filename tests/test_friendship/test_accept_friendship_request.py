from __future__ import annotations

from unittest.mock import patch

import dirty_equals
import pytest
from sqlalchemy import select

from src.friendship.enums import FriendshipRequestStatus
from src.friendship.models import Friendship, FriendshipRequest
from src.shared.database import Base
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_friendship_request"})
async def test_accept_friendship_request_returns_201_with_correct_response(f):
    result = await f.client.put(
        "/friendship/requests/1/accepted",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 201
    assert result.json() == {
        "friendships": [
            {
                "account_id": 1,
                "created_at": dirty_equals.IsDatetime(format_string="%Y-%m-%dT%H:%M:%S.%fZ"),
                "friend_id": 2,
            },
            {
                "account_id": 2,
                "created_at": dirty_equals.IsDatetime(format_string="%Y-%m-%dT%H:%M:%S.%fZ"),
                "friend_id": 1,
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_friendship_request"})
async def test_accept_friendship_request_creates_objects_in_db_correctly(f):
    result = await f.client.put(  # noqa: F841
        "/friendship/requests/1/accepted",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    with patch.object(Base, "__eq__", __eq__):
        friendship_requests = (await f.db.execute(select(FriendshipRequest))).scalars().all()
        assert friendship_requests == [
            FriendshipRequest(
                id=1,
                created_at=dirty_equals.IsDatetime(enforce_tz=True),
                receiver_id=2,
                sender_id=1,
                status=FriendshipRequestStatus.ACCEPTED,
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
            ),
        ]
        friendships = (await f.db.execute(select(Friendship).order_by(Friendship.account_id))).scalars().all()
        assert friendships == [
            Friendship(
                account_id=1,
                created_at=dirty_equals.IsDatetime(enforce_tz=True),
                friend_id=2,
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
            ),
            Friendship(
                account_id=2,
                created_at=dirty_equals.IsDatetime(enforce_tz=True),
                friend_id=1,
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_friendship_request_from_another_user",
})
async def test_accept_friendship_request_with_friendship_request_from_another_user_returns_403_with_correct_response(f):
    result = await f.client.put(
        "/friendship/requests/1/accepted",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Accept friendship request.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
