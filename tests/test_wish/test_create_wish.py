from __future__ import annotations

from unittest.mock import patch
from uuid import UUID

import dirty_equals
import httpx
import pytest
from sqlalchemy import select
from wlss.shared.types import Id
from wlss.wish.types import WishDescription, WishTitle

from api.wish.dtos import CreateWishRequest, CreateWishResponse
from src.shared.database import Base
from src.wish.models import Wish
from tests.utils.dirty_equals import IsId, IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_one_file"})
async def test_create_wish_returns_correct_response(f):
    result = await f.api.wish.create_wish(
        account_id=Id(1),
        token=f.access_token,
        request_data=CreateWishRequest.model_validate({
            "title": "Horse",
            "description": "I'm gonna take my horse to the old town road.",
            "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
        }),
    )

    assert isinstance(result, CreateWishResponse)
    assert result.model_dump() == {
        "id": dirty_equals.IsInt,
        "account_id": 1,
        "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
        "created_at": IsUtcDatetimeSerialized,
        "description": "I'm gonna take my horse to the old town road.",
        "title": "Horse",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_one_file"})
async def test_create_wish_creates_objects_in_db_correctly(f):
    result = await f.api.wish.create_wish(  # noqa: F841
        account_id=Id(1),
        token=f.access_token,
        request_data=CreateWishRequest.model_validate({
            "title": "Horse",
            "description": "I'm gonna take my horse to the old town road.",
            "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
        }),
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
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts_and_one_file"})
async def test_create_wish_with_another_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.create_wish(
            account_id=Id(2),
            token=f.access_token,
            request_data=CreateWishRequest.model_validate({
                "title": "Horse",
                "description": "I'm gonna take my horse to the old town road.",
                "avatar_id": "0b928aaa-521f-47ec-8be5-396650e2a187",
            }),
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Create wish.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }
