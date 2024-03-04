from __future__ import annotations

import pytest
from wlss.shared.types import Id

from api.profile.dtos import GetProfileResponse


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_profile_and_one_file", "access_token": "access_token"})
async def test_get_profile_returns_correct_response(f):
    result = await f.api.profile.get_profile(account_id=Id(1), token=f.access_token)

    assert isinstance(result, GetProfileResponse)
    assert result.model_dump() == {
        "account_id": 1,
        "avatar_id": None,
        "description": None,
        "name": "John Doe",
    }
