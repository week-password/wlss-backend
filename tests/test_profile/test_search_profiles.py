from __future__ import annotations

import pytest

from api.profile.dtos import SearchProfilesResponse


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_three_profiles"})
async def test_search_profiles_returns_correct_response(f):
    result = await f.api.profile.search_profiles(token=f.access_token)

    assert isinstance(result, SearchProfilesResponse)
    assert result.model_dump() == {
        "profiles": [
            {
                "account_id": 3,
                "avatar_id": None,
                "description": None,
                "name": "John Bloggs",
            },
            {
                "account_id": 2,
                "avatar_id": None,
                "description": None,
                "name": "John Smith",
            },
            {
                "account_id": 1,
                "avatar_id": None,
                "description": None,
                "name": "John Doe",
            },
        ],
    }
