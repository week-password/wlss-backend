from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_profile_and_one_file", "access_token": "access_token"})
async def test_get_profile_returns_200_with_correct_response(f):
    result = await f.client.get("/accounts/1/profile", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 200
    assert result.json() == {
        "account_id": 1,
        "avatar_id": None,
        "description": None,
        "name": "John Doe",
    }
