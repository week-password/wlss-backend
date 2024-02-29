from __future__ import annotations

from datetime import datetime

import dirty_equals
import jwt
import pytest

from src.config import CONFIG
from src.shared.datetime import DATETIME_FORMAT
from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "refresh_token": "refresh_token",
    "db": "db_with_one_account_and_one_session",
})
async def test_refresh_tokens_returns_201_with_correct_response(f):
    result = await f.client.post(
        "/accounts/1/sessions/b9dd3a32-aee8-4a6b-a519-def9ca30c9ec/tokens",
        headers={"Authorization": f"Bearer {f.refresh_token}"},
    )

    assert result.status_code == 201
    json = result.json()
    assert json == {
        "access_token": dirty_equals.IsStr,
        "refresh_token": dirty_equals.IsStr,
    }
    access_token_payload = jwt.decode(json["access_token"], CONFIG.SECRET_KEY, "HS256")
    assert access_token_payload == {
        "account_id": 1,
        "expires_at": IsUtcDatetimeSerialized,
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    refresh_token_payload = jwt.decode(json["refresh_token"], CONFIG.SECRET_KEY, "HS256")
    assert refresh_token_payload == {
        "account_id": 1,
        "expires_at": IsUtcDatetimeSerialized,
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    access_token_expiration = datetime.strptime(  # noqa: DTZ007
        access_token_payload["expires_at"], DATETIME_FORMAT,
    )
    refresh_token_expiration = datetime.strptime(  # noqa: DTZ007
        refresh_token_payload["expires_at"],
        DATETIME_FORMAT,
    )
    assert access_token_expiration < refresh_token_expiration


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "refresh_token": "refresh_token_expired",
    "db": "db_with_one_account_and_one_session",
})
async def test_refresh_tokens_with_expired_token_returns_401_with_correct_response(f):
    result = await f.client.post(
        "/accounts/1/sessions/b9dd3a32-aee8-4a6b-a519-def9ca30c9ec/tokens",
        headers={"Authorization": f"Bearer {f.refresh_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Token validation",
        "description": "Token expired.",
        "details": "Provided token is expired.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "client": "client",
    "refresh_token": "refresh_token",
    "db": "db_with_one_account_and_one_session",
})
async def test_refresh_tokens_with_account_different_than_current_returns_403_with_correct_response(f):
    result = await f.client.post(
        "/accounts/42/sessions/b9dd3a32-aee8-4a6b-a519-def9ca30c9ec/tokens",
        headers={"Authorization": f"Bearer {f.refresh_token}"},
    )

    assert result.status_code == 403
    assert result.json() == {
        "action": "Refresh tokens",
        "description": "Requested action not allowed.",
        "details": "Provided tokens or credentials don't grant you enough access rights.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "refresh_token": "refresh_token", "db": "db_empty"})
async def test_refresh_tokens_with_different_session_ids_in_url_path_and_token_returns_401_with_correct_response(f):
    result = await f.client.post(
        "/accounts/1/sessions/00000000-0000-0000-0000-000000000000/tokens",
        headers={"Authorization": f"Bearer {f.refresh_token}"},
    )

    assert result.status_code == 401
    assert result.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "refresh_token": "refresh_token", "db": "db_with_one_account"})
async def test_refresh_tokens_with_invalid_token_returns_401_with_correct_response(f):
    result = await f.client.post(
        "/accounts/1/sessions/b9dd3a32-aee8-4a6b-a519-def9ca30c9ec/tokens",
        headers={"Authorization": "Bearer invalid token"},
    )

    assert result.status_code == 401
    assert result.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_refresh_tokens_with_nonexistent_session_returns_401_with_correct_response(f):
    payload = {
        "account_id": 1,
        "created_at": "2023-06-17T11:47:02.823Z",
        "session_id": "42424242-aee8-4a6b-a519-def9ca30c9ec",
    }
    token = jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")

    result = await f.client.post(
        "/accounts/1/sessions/42424242-aee8-4a6b-a519-def9ca30c9ec/tokens",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert result.status_code == 401
    assert result.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }
