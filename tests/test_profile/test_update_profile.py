from __future__ import annotations

from unittest.mock import patch
from uuid import UUID

import dirty_equals
import pytest
from sqlalchemy import select

from src.profile.models import Profile
from src.shared.database import Base
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_profile_and_one_file", "access_token": "access_token"})
async def test_update_profile_returns_200_with_correct_response(f):
    result = await f.client.put(
        "/accounts/1/profile",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "avatar_id": "2b41c87b-6f06-438b-9933-2a1568cc593b",
            "description": "Updated description.",
            "name": "Updated name.",
        },
    )

    assert result.status_code == 200
    assert result.json() == {
        "account_id": 1,
        "avatar_id": "2b41c87b-6f06-438b-9933-2a1568cc593b",
        "description": "Updated description.",
        "name": "Updated name.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_profile_and_one_file", "access_token": "access_token"})
async def test_update_profile_updates_profile_in_db_correctly(f):
    result = await f.client.put(  # noqa: F841
        "/accounts/1/profile",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "avatar_id": "2b41c87b-6f06-438b-9933-2a1568cc593b",
            "description": "Updated description.",
            "name": "Updated name.",
        },
    )

    with patch.object(Base, "__eq__", __eq__):
        profiles = (await f.db.execute(select(Profile))).scalars().all()
        assert profiles == [
            Profile(
                account_id=1,
                avatar_id=UUID("2b41c87b-6f06-438b-9933-2a1568cc593b"),
                description="Updated description.",
                name="Updated name.",
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
            ),
        ]
