from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({"access_token": "access_token", "client": "client", "db": "db_with_one_account_and_one_session"})
async def test_get_account_id_returns_200_with_correct_response(f):
    result = await f.client.get("/accounts/logins/john_doe/id", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 200
    assert result.json() == {"id": 1}


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_expired",
    "client": "client",
    "db": "db_with_one_account_and_one_session",
})
async def test_get_account_id_with_expired_token_returns_403_with_correct_response(f):
    result = await f.client.get("/accounts/logins/john_doe/id", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 403
    assert result.json() == {
        "action": "Token validation",
        "description": "Token expired.",
        "details": "Provided token is expired.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token_with_nonexistent_account",
    "client": "client",
    "db": "db_with_one_account_and_one_session"})
async def test_get_account_id_with_nonexistent_account_in_token_payload_returns_401_with_correct_response(f):
    result = await f.client.get("/accounts/logins/john_doe/id", headers={"Authorization": f"Bearer {f.access_token}"})

    assert result.status_code == 401
    assert result.json() == {
        "description": "Request initiator is not authenticated.",
        "details": "Your credentials or tokens are invalid or missing.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_one_account_and_one_session",
})
async def test_get_account_id_with_nonexistent_account_returns_404_with_correct_response(f):
    result = await f.client.get(
        "/accounts/logins/john_doe_nonexistent/id",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 404
    assert result.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
