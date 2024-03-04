from __future__ import annotations

import pytest
from wlss.shared.types import Id

from api.friendship.dtos import GetAccountFriendshipsResponse
from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_friendships"})
async def test_get_account_friendships_returns_correct_response(f):
    result = await f.api.friendship.get_account_friendships(account_id=Id(1), token=f.access_token)

    assert isinstance(result, GetAccountFriendshipsResponse)
    assert result.model_dump() == {
        "friendships": [
            {
                "account_id": 1,
                "created_at": IsUtcDatetimeSerialized,
                "friend_id": 2,
            },
        ],
    }
