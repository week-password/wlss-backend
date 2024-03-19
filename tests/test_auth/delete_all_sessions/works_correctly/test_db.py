from __future__ import annotations

import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.auth.models import Session


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_two_sessions"})
async def test(f):
    result = await f.api.auth.delete_all_sessions(account_id=Id(1), token=f.access_token)  # noqa: F841

    rows = (await f.db.execute(select(Session))).all()
    assert not rows
