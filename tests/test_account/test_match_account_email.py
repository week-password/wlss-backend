from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_match_account_email_returns_204_with_correct_response(f):
    result = await f.client.post(
        "/accounts/emails/match",
        json={"email": "john.doe@mail.com"},
        headers={"Authorization": "Bearer token"},
    )

    assert result.status_code == 204
    assert result.content == b""


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_empty"})
async def test_match_account_email_with_nonexistent_account_email_returns_404_with_correct_response(f):
    result = await f.client.post(
        "/accounts/emails/match",
        json={"email": "john.doe@mail.com"},
        headers={"Authorization": "Bearer token"},
    )

    assert result.status_code == 404
    assert result.status_code == 404
    assert result.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
