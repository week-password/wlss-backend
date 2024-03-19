from __future__ import annotations

import pytest

from api.account.dtos import MatchAccountEmailRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test(f):
    result = await f.api.account.match_account_email(request_data=MatchAccountEmailRequest(email="john.doe@mail.com"))

    assert result
