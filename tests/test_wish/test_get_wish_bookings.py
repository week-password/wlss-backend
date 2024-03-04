from __future__ import annotations

import httpx
import pytest
from wlss.shared.types import Id

from api.wish.dtos import GetWishBookingsResponse
from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_get_wish_bookings_returns_correct_response(f):
    result = await f.api.wish.get_wish_bookings(account_id=Id(2), token=f.access_token)

    assert isinstance(result, GetWishBookingsResponse)
    assert result.model_dump() == {
        "wish_bookings": [
            {
                "id": 1,
                "account_id": 1,
                "created_at": IsUtcDatetimeSerialized,
                "wish_id": 1,
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_two_friend_accounts_and_one_wish_booking",
})
async def test_get_wish_bookings_with_same_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.get_wish_bookings(account_id=Id(1), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Get wish bookings.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
