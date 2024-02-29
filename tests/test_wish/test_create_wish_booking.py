from __future__ import annotations

from unittest.mock import patch

import dirty_equals
import pytest
from sqlalchemy import select

from src.shared.database import Base
from src.wish.models import WishBooking
from tests.utils.mocks.models import __eq__


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
    "db": "db_with_two_friend_accounts_and_one_wish",
})
async def test_create_wish_booking_creates_objects_in_db_correctly(f):
    result = await f.client.post(  # noqa: F841
        "/accounts/2/wishes/1/bookings",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={"account_id": 1, "wish_id": 1},
    )

    with patch.object(Base, "__eq__", __eq__):
        wish_bookings = (await f.db.execute(select(WishBooking))).scalars().all()
        assert wish_bookings == [
            WishBooking(
                id=dirty_equals.IsPositiveInt,
                account_id=1,
                created_at=dirty_equals.IsDatetime(enforce_tz=True),
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
                wish_id=1,
            ),
        ]


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
