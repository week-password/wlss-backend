from __future__ import annotations

from unittest.mock import patch
from uuid import UUID

import httpx
import pytest
from sqlalchemy import select
from wlss.file.types import FileName, FileSize
from wlss.shared.types import Id

from api.file.enums import Extension, MimeType
from src.file.models import File
from src.shared.database import Base
from src.wish.models import Wish
from tests.utils.dirty_equals import IsUtcDatetime
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_wish",
    "redis": "redis_with_one_session",
})
async def test_delete_wish_returns_correct_response(f):
    result = await f.api.wish.delete_wish(account_id=Id(1), wish_id=Id(1), token=f.access_token)

    assert result is None


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_wish",
    "redis": "redis_with_one_session",
})
async def test_delete_wish_deletes_objects_from_db_correctly(f):
    result = await f.api.wish.delete_wish(account_id=Id(1), wish_id=Id(1), token=f.access_token)  # noqa: F841

    with patch.object(Base, "__eq__", __eq__):
        wishes = (await f.db.execute(select(Wish))).all()
        assert wishes == []
        files = (await f.db.execute(select(File))).scalars().all()
        assert files == [
            File(
                id=UUID("0b928aaa-521f-47ec-8be5-396650e2a187"),
                extension=Extension.PNG,
                mime_type=MimeType.IMAGE_PNG,
                name=FileName("image.png"),
                size=FileSize(17),
                created_at=IsUtcDatetime,
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_two_accounts_and_one_wish",
    "redis": "redis_with_one_session",
})
async def test_delete_wish_with_another_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.wish.delete_wish(account_id=Id(2), wish_id=Id(1), token=f.access_token)

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Delete wish.",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_one_wish_without_avatar",
    "redis": "redis_with_one_session",
})
async def test_delete_wish_without_avatar_returns_204_with_correct_response(f):
    result = await f.api.wish.delete_wish(account_id=Id(1), wish_id=Id(1), token=f.access_token)

    assert result is None
