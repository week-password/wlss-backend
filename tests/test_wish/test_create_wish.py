from __future__ import annotations

from unittest.mock import patch
from uuid import UUID

import dirty_equals
import pytest
from sqlalchemy import select
from wlss.shared.types import Id
from wlss.wish.types import WishDescription, WishTitle

from src.shared.database import Base
from src.wish.models import Wish
from tests.utils.dirty_equals import IsId, IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_account_and_one_file"})
async def test_create_wish_returns_201_with_correct_response(f):
    result = await f.client.post(
        "/accounts/1/wishes",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "title": "Horse",
            "description": "I'm gonna take my horse to the old town road.",
            "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
        },
    )

    assert result.status_code == 201
    assert result.json() == {
        "id": dirty_equals.IsInt,
        "account_id": 1,
        "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
        "created_at": IsUtcDatetimeSerialized,
        "description": "I'm gonna take my horse to the old town road.",
        "title": "Horse",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_account_and_one_file"})
async def test_create_wish_creates_objects_in_db_correctly(f):
    result = await f.client.post(  # noqa: F841
        "/accounts/1/wishes",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "title": "Horse",
            "description": "I'm gonna take my horse to the old town road.",
            "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
        },
    )

    with patch.object(Base, "__eq__", __eq__):
        wishes = (await f.db.execute(select(Wish))).scalars().all()
        assert wishes == [
            Wish(
                id=IsId,
                account_id=Id(1),
                avatar_id=UUID("0b928aaa-521f-47ec-8be5-396650e2a187"),
                created_at=IsUtcDatetime,
                description=WishDescription("I'm gonna take my horse to the old town road."),
                title=WishTitle("Horse"),
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts_and_one_file"})
async def test_create_wish_with_another_account_returns_403_with_correct_response(f):
    result = await f.client.post(
        "/accounts/2/wishes",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "title": "Horse",
            "description": "I'm gonna take my horse to the old town road.",
            "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
        },
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Create wish.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
