from __future__ import annotations

import dirty_equals
import pytest

from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_three_accounts_and_three_friendship_requests",
})
async def test_get_friendship_requests_returns_200_with_correct_response(f):
    result = await f.client.get(
        "/accounts/1/friendship/requests",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 200
    assert result.json() == {
        "requests": [
            {
                "id": dirty_equals.IsInt,
                "created_at": IsUtcDatetimeSerialized,
                "receiver_id": 2,
                "sender_id": 1,
                "status": "PENDING",
            },
            {
                "id": dirty_equals.IsInt,
                "created_at": IsUtcDatetimeSerialized,
                "receiver_id": 1,
                "sender_id": 3,
                "status": "PENDING",
            },
        ],
    }
