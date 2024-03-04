from __future__ import annotations

from unittest.mock import patch

import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from api.wish.dtos import CreateWishBookingRequest, CreateWishBookingResponse
from src.shared.database import Base
from src.wish.models import WishBooking
from tests.utils.dirty_equals import IsId, IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_friend_accounts_and_one_wish"})
async def test_create_wish_booking_returns_correct_response(f):
    result = await f.api.wish.create_wish_booking(
        account_id=Id(2),
        wish_id=Id(1),
        token=f.access_token,
        request_data=CreateWishBookingRequest.model_validate({"account_id": 1, "wish_id": 1}),
    )

    assert isinstance(result, CreateWishBookingResponse)
    assert result.model_dump() == {
        "account_id": 1,
        "created_at": IsUtcDatetimeSerialized,
        "wish_id": 1,
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_friend_accounts_and_one_wish"})
async def test_create_wish_booking_creates_objects_in_db_correctly(f):
    result = await f.api.wish.create_wish_booking(  # noqa: F841
        account_id=Id(2),
        wish_id=Id(1),
        token=f.access_token,
        request_data=CreateWishBookingRequest.model_validate({"account_id": 1, "wish_id": 1}),
    )

    with patch.object(Base, "__eq__", __eq__):
        wish_bookings = (await f.db.execute(select(WishBooking))).scalars().all()
        assert wish_bookings == [
            WishBooking(
                id=IsId,
                account_id=Id(1),
                created_at=IsUtcDatetime,
                updated_at=IsUtcDatetime,
                wish_id=Id(1),
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts_and_one_wish"})
async def test_create_wish_booking_for_non_friend_account_returns_403_with_correct_response(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.create_wish_booking(
            account_id=Id(2),
            wish_id=Id(1),
            request_data=CreateWishBookingRequest.model_validate({"account_id": 1, "wish_id": 1}),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Create wish booking.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
