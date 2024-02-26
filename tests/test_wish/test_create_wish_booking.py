from __future__ import annotations

import dirty_equals
import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_two_friend_accounts_and_one_wish",
})
async def test_create_wish_booking_returns_201_with_correct_response(f):
    result = await f.client.post(
        "/accounts/2/wishes/1/bookings",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={"account_id": 1, "wish_id": 1},
    )

    assert result.status_code == 201
    assert result.json() == {
        "account_id": 1,
        "created_at": dirty_equals.IsDatetime(format_string="%Y-%m-%dT%H:%M:%S.%fZ"),
        "wish_id": 1,
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_two_accounts_and_one_wish",
})
async def test_create_wish_booking_for_non_friend_account_returns_403_with_correct_response(f):
    result = await f.client.post(
        "/accounts/2/wishes/1/bookings",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={"account_id": 1, "wish_id": 1},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Create wish booking.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
