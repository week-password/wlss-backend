from __future__ import annotations

import httpx
import pytest
from wlss.shared.types import Id

from api.wish.dtos import GetAccountWishesResponse
from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_two_accounts_and_two_wishes"})
async def test_get_account_wishes_returns_correct_response(f):
    result = await f.api.wish.get_account_wishes(account_id=Id(1), token=f.access_token)

    assert isinstance(result, GetAccountWishesResponse)
    assert result.model_dump() == {
        "wishes": [
            {
                "id": 2,
                "account_id": 1,
                "avatar_id": "4b94605b-f5e1-40b1-b9fc-c635c9529e3e",
                "created_at": IsUtcDatetimeSerialized,
                "description": "I need some sleep. Time to put the old horse down.",
                "title": "Sleep",
            },
            {
                "id": 1,
                "account_id": 1,
                "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
                "created_at": IsUtcDatetimeSerialized,
                "description": "I'm gonna take my horse to the old town road.",
                "title": "Horse",
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts_and_two_wishes"})
async def test_get_account_wishes_from_not_friend_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.get_account_wishes(account_id=Id(2), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Get wishes.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
