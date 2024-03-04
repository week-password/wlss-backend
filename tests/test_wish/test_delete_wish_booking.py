from __future__ import annotations

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.wish.models import WishBooking


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_delete_wish_booking_returns_correct_response(f):
    result = await f.api.wish.delete_wish_booking(
        account_id=Id(2),
        wish_id=Id(1),
        booking_id=Id(1),
        token=f.access_token,
    )

    assert result is None


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_delete_wish_booking_deletes_objects_from_db_correctly(f):
    result = await f.api.wish.delete_wish_booking(  # noqa: F841
        account_id=Id(2),
        wish_id=Id(1),
        booking_id=Id(1),
        token=f.access_token,
    )

    wish_bookings = (await f.db.execute(select(WishBooking))).all()
    assert wish_bookings == []


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_delete_wish_booking_with_nonexistent_booking_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.delete_wish_booking(
            account_id=Id(2),
            wish_id=Id(1),
            booking_id=Id(2),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "Wish booking",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_delete_wish_booking_with_wish_created_by_self_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.delete_wish_booking(
            account_id=Id(1),
            wish_id=Id(1),
            booking_id=Id(1),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete wish booking.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_for_another_account",
    "api": "api",
    "db": "db_with_three_friend_accounts_and_one_booking",
})
async def test_delete_wish_booking_with_booking_created_by_other_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.delete_wish_booking(
            account_id=Id(2),
            wish_id=Id(1),
            booking_id=Id(1),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete wish booking.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
