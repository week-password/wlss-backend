from __future__ import annotations

import pytest

from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts_and_two_wishes"})
async def test_get_account_wishes_returns_200_with_correct_response(f):
    result = await f.client.get(
        "/accounts/1/wishes",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 200
    assert result.json() == {
        "wishes": [
            {
                "id": 1,
                "account_id": 1,
                "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
                "created_at": IsUtcDatetimeSerialized,
                "description": "I'm gonna take my horse to the old town road.",
                "title": "Horse",
            },
            {
                "id": 2,
                "account_id": 1,
                "avatar_id": "4b94605b-f5e1-40b1-b9fc-c635c9529e3e",
                "created_at": IsUtcDatetimeSerialized,
                "description": "I need some sleep. Time to put the old horse down.",
                "title": "Sleep",
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts_and_two_wishes"})
async def test_get_account_wishes_from_not_friend_account_returns_403_with_correct_response(f):
    result = await f.client.get(
        "/accounts/2/wishes",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Get wishes.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
