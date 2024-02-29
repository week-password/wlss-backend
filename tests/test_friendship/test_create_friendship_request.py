from __future__ import annotations

from unittest.mock import patch

import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.friendship.enums import FriendshipRequestStatus
from src.friendship.models import FriendshipRequest
from src.shared.database import Base
from tests.utils.dirty_equals import IsId, IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts"})
async def test_create_friendship_request_returns_201_with_correct_response(f):
    result = await f.client.post(
        "/friendship/requests",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={"receiver_id": 2, "sender_id": 1},
    )

    assert result.status_code == 201
    assert result.json() == {
        "id": 10000,
        "created_at": IsUtcDatetimeSerialized,
        "receiver_id": 2,
        "sender_id": 1,
        "status": "PENDING",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts"})
async def test_create_friendship_request_creates_objects_in_db_correctly(f):
    result = await f.client.post(  # noqa: F841
        "/friendship/requests",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={"receiver_id": 2, "sender_id": 1},
    )

    with patch.object(Base, "__eq__", __eq__):
        friendship_requests = (await f.db.execute(select(FriendshipRequest))).scalars().all()
        assert friendship_requests == [
            FriendshipRequest(
                id=IsId,
                created_at=IsUtcDatetime,
                receiver_id=Id(2),
                sender_id=Id(1),
                status=FriendshipRequestStatus.PENDING,
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts"})
async def test_create_friendship_request_for_different_account_ids_in_query_and_token_returns_403_with_correct_response(
    f,
):
    result = await f.client.post(
        "/friendship/requests",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={"receiver_id": 1, "sender_id": 2},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Create friendship request.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
