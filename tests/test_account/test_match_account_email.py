from __future__ import annotations

import httpx
import pytest

from api.account.dtos import MatchAccountEmailRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_match_account_email_returns_correct_response(f):
    result = await f.api.account.match_account_email(request_data=MatchAccountEmailRequest(email="john.doe@mail.com"))

    assert result


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_empty"})
async def test_match_account_email_with_nonexistent_account_email_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.match_account_email(
            request_data=MatchAccountEmailRequest.model_validate({"email": "john.doe@mail.com"}),
        )

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
