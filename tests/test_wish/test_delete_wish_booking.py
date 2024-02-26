from __future__ import annotations

import pytest
from sqlalchemy import select

from src.wish.models import WishBooking


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_delete_wish_booking_returns_204_with_correct_response(f):
    result = await f.client.delete(
        "/bookings/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 204
    assert result.content == b""


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_delete_wish_booking_deletes_objects_from_db_correctly(f):
    result = await f.client.delete(  # noqa: F841
        "/bookings/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    wish_bookings = (await f.db.execute(select(WishBooking))).all()
    assert wish_bookings == []


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_delete_wish_booking_with_nonexistent_booking_returns_404_with_correct_response(f):
    result = await f.client.delete(
        "/bookings/2",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 404
    assert result.json() == {
        "resource": "Wish booking",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
