from __future__ import annotations

import httpx
import pytest
from wlss.account.types import AccountLogin

from api.account.dtos import GetAccountIdResponse


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "access_token": "access_token", "db": "db_with_one_account_and_one_session"})
async def test_get_account_id_returns_correct_response(f):
    result = await f.api.account.get_account_id(account_login=AccountLogin("john_doe"), token=f.access_token)

    assert isinstance(result, GetAccountIdResponse)
    assert result.model_dump() == {"id": 1}


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_expired",
    "api": "api",
    "db": "db_with_one_account_and_one_session",
})
async def test_get_account_id_with_expired_token_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_account_id(
            account_login=AccountLogin("john_doe"),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 403
    assert exc_info.value.response.json() == {
        "action": "Token validation",
        "description": "Token expired.",
        "details": "Provided token is expired.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_with_nonexistent_account",
    "api": "api",
    "db": "db_with_one_account_and_one_session"})
async def test_get_account_id_with_nonexistent_account_in_token_payload_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_account_id(
            account_login=AccountLogin("john_doe"),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 401
    assert exc_info.value.response.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_one_account_and_one_session",
})
async def test_get_account_id_with_nonexistent_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_account_id(
            account_login=AccountLogin("john_doe_nonexistent"),
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
