from __future__ import annotations

import pytest

from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_get_wish_bookings_returns_200_with_correct_response(f):
    result = await f.client.get(
        "/accounts/2/wishes/bookings?wish_id=1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 200
    assert result.json() == {
        "wish_bookings": [
            {
                "account_id": 1,
                "created_at": IsUtcDatetimeSerialized,
                "wish_id": 1,
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_get_wish_bookings_with_same_account_returns_403_with_correct_response(f):
    result = await f.client.get(
        "/accounts/1/wishes/bookings?wish_id=1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Get wish bookings.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
