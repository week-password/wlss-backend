from __future__ import annotations

import httpx
import pytest
from wlss.account.types import AccountLogin
from wlss.shared.types import Id

from api.account.dtos import GetAccountsResponse


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "api": "api", "db": "db_with_two_accounts"})
async def test_get_accounts_returns_correct_response(f):
    result = await f.api.account.get_accounts(
        account_ids=[Id(1)],
        account_logins=[AccountLogin("john_smith")],
        token=f.access_token,
    )

    assert isinstance(result, GetAccountsResponse)
    assert result.model_dump() == {
        "accounts": [
            {"id": 1, "login": "john_doe"},
            {"id": 2, "login": "john_smith"},
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_incorrect",
    "api": "api",
    "db": "db_with_one_account_and_one_session",
})
async def test_get_accounts_with_incorrect_token_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_accounts(
            account_logins=[AccountLogin("john_doe")],
            token=f.access_token,
        )

    assert exc_info.value.response.status_code == 422
    assert exc_info.value.response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["created_at"],
                "msg": "Field required",
                "input": {
                    "account_id": 1,
                    "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
                },
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_expired",
    "api": "api",
    "db": "db_with_one_account_and_one_session",
})
async def test_get_accounts_with_expired_token_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_accounts(
            account_logins=[AccountLogin("john_doe")],
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
async def test_get_accounts_with_nonexistent_account_in_token_payload_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.get_accounts(account_logins=[AccountLogin("john_doe")], token=f.access_token)

    assert exc_info.value.response.status_code == 401
    assert exc_info.value.response.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }
