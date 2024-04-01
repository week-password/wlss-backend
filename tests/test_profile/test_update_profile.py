from __future__ import annotations

from unittest.mock import patch
from uuid import UUID

import pytest
from sqlalchemy import select
from wlss.profile.types import ProfileDescription, ProfileName
from wlss.shared.types import Id

from api.profile.dtos import UpdateProfileRequest, UpdateProfileResponse
from src.profile.models import Profile
from src.shared.database import Base
from tests.utils.dirty_equals import IsUtcDatetime
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_profile_and_one_file", "access_token": "access_token"})
async def test_update_profile_returns_correct_response(f):
    result = await f.api.profile.update_profile(
        account_id=Id(1),
        request_data=UpdateProfileRequest.model_validate({
            "avatar_id": "2b41c87b-6f06-438b-9933-2a1568cc593b",
            "description": "Updated description.",
            "name": "Updated name.",
        }),
        token=f.access_token,
    )

    assert isinstance(result, UpdateProfileResponse)
    assert result.model_dump() == {
        "account_id": 1,
        "avatar_id": "2b41c87b-6f06-438b-9933-2a1568cc593b",
        "description": "Updated description.",
        "name": "Updated name.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_profile_and_one_file", "access_token": "access_token"})
async def test_update_profile_updates_profile_in_db_correctly(f):
    result = await f.api.profile.update_profile(  # noqa: F841
        account_id=Id(1),
        request_data=UpdateProfileRequest.model_validate({
            "avatar_id": "2b41c87b-6f06-438b-9933-2a1568cc593b",
            "description": "Updated description.",
            "name": "Updated name.",
        }),
        token=f.access_token,
    )

    with patch.object(Base, "__eq__", __eq__):
        profiles = (await f.db.execute(select(Profile))).scalars().all()
        assert profiles == [
            Profile(
                account_id=Id(1),
                avatar_id=UUID("2b41c87b-6f06-438b-9933-2a1568cc593b"),
                created_at=IsUtcDatetime,
                description=ProfileDescription("Updated description."),
                name=ProfileName("Updated name."),
                updated_at=IsUtcDatetime,
            ),
        ]
