from __future__ import annotations

import pytest

from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_friendships"})
async def test_get_account_friendships_returns_200_with_correct_response(f):
    result = await f.client.get("/accounts/1/friendships", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 200
    assert result.json() == {
        "friendships": [
            {
                "account_id": 1,
                "created_at": IsUtcDatetimeSerialized,
                "friend_id": 2,
            },
        ],
    }
