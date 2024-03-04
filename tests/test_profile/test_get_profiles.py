from __future__ import annotations

import pytest
from wlss.shared.types import Id

from api.profile.dtos import GetProfilesResponse


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_three_profiles"})
async def test_get_profiles_returns_correct_response(f):
    result = await f.api.profile.get_profiles(account_ids=[Id(1), Id(2)], token=f.access_token)

    assert isinstance(result, GetProfilesResponse)
    assert result.model_dump() == {
        "profiles": [
            {
                "account_id": 1,
                "avatar_id": None,
                "description": None,
                "name": "John Doe",
            },
            {
                "account_id": 2,
                "avatar_id": None,
                "description": None,
                "name": "John Smith",
            },
        ],
    }
