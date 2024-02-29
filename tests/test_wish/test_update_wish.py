from __future__ import annotations

from unittest.mock import patch
from uuid import UUID

import pytest
from sqlalchemy import select
from wlss.shared.types import Id
from wlss.wish.types import WishDescription, WishTitle

from src.shared.database import Base
from src.wish.models import Wish
from tests.utils.dirty_equals import IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_files_and_one_wish"})
async def test_update_wish_returns_200_with_correct_response(f):
    result = await f.client.put(
        "/accounts/1/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "title": "NEW Horse",
            "description": "I'm gonna take my NEW horse to the old town road.",
            "avatar_id": "4b94605b-f5e1-40b1-b9fc-c635c9529e3e",
        },
    )

    assert result.status_code == 200
    assert result.json() == {
        "id": 1,
        "account_id": 1,
        "avatar_id": "4b94605b-f5e1-40b1-b9fc-c635c9529e3e",
        "created_at": IsUtcDatetimeSerialized,
        "description": "I'm gonna take my NEW horse to the old town road.",
        "title": "NEW Horse",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_files_and_one_wish"})
async def test_update_wish_updates_objects_in_db_correctly(f):
    result = await f.client.put(  # noqa: F841
        "/accounts/1/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "title": "NEW Horse",
            "description": "I'm gonna take my NEW horse to the old town road.",
            "avatar_id": "4b94605b-f5e1-40b1-b9fc-c635c9529e3e",
        },
    )

    with patch.object(Base, "__eq__", __eq__):
        wishes = (await f.db.execute(select(Wish))).scalars().all()
        assert wishes == [
            Wish(
                id=Id(1),
                account_id=Id(1),
                avatar_id=UUID("4b94605b-f5e1-40b1-b9fc-c635c9529e3e"),
                created_at=IsUtcDatetime,
                description=WishDescription("I'm gonna take my NEW horse to the old town road."),
                title=WishTitle("NEW Horse"),
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_account_and_one_file"})
async def test_update_wish_with_nonexistent_wish_returns_404_with_correct_response(f):
    result = await f.client.put(
        "/accounts/1/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "title": "NEW Horse",
            "description": "I'm gonna take my NEW horse to the old town road.",
            "avatar_id": "4b94605b-f5e1-40b1-b9fc-c635c9529e3e",
        },
    )

    assert result.status_code == 404
    assert result.json() == {
        "resource": "Wish",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_two_accounts_and_one_file"})
async def test_update_wish_with_another_account_returns_403_with_correct_response(f):
    result = await f.client.put(
        "/accounts/2/wishes/1",
        headers={"Authorization": f"Bearer {f.access_token}"},
        json={
            "title": "NEW Horse",
            "description": "I'm gonna take my NEW horse to the old town road.",
            "avatar_id": "4b94605b-f5e1-40b1-b9fc-c635c9529e3e",
        },
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Update wish.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
