from __future__ import annotations

from unittest.mock import patch

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from api.friendship.dtos import CreateFriendshipRequestRequest, CreateFriendshipRequestResponse
from api.friendship.enums import FriendshipRequestStatus
from src.friendship.models import FriendshipRequest
from src.shared.database import Base
from tests.utils.dirty_equals import IsId, IsIdSerialized, IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_accounts"})
async def test_create_friendship_request_correct_response(f):
    result = await f.api.friendship.create_friendship_request(
        request_data=CreateFriendshipRequestRequest.model_validate({"receiver_id": 2, "sender_id": 1}),
        token=f.access_token,
    )

    assert isinstance(result, CreateFriendshipRequestResponse)
    assert result.model_dump() == {
        "id": IsIdSerialized,
        "created_at": IsUtcDatetimeSerialized,
        "receiver_id": 2,
        "sender_id": 1,
        "status": FriendshipRequestStatus.PENDING,
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_accounts"})
async def test_create_friendship_request_creates_objects_in_db_correctly(f):
    result = await f.api.friendship.create_friendship_request(  # noqa: F841
        request_data=CreateFriendshipRequestRequest.model_validate({"receiver_id": 2, "sender_id": 1}),
        token=f.access_token,
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
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts"})
async def test_create_friendship_request_for_different_account_ids_in_query_and_token_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.friendship.create_friendship_request(
            request_data=CreateFriendshipRequestRequest.model_validate({"receiver_id": 1, "sender_id": 2}),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Create friendship request.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
