from __future__ import annotations

import pytest

from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_friendships"})
async def test_get_friends_returns_200_with_correct_response(f):
    result = await f.client.get("/accounts/1/friends", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 200
    assert result.json() == {
        "friends": [
            {
                "account": {
                    "id": 2,
                },
                "profile": {
                    "account_id": 2,
                    "avatar_id": None,
                    "description": None,
                    "name": "John Smith",
                },
                "friendship": {
                    "created_at": IsUtcDatetimeSerialized,
                },
            },
        ],
    }
