from __future__ import annotations

import httpx
import pytest

from api.account.dtos import CreateAccountRequest


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.account.create_account(
            request_data=CreateAccountRequest.model_validate({
                "account": {
                    "email": "john.doe@mail.com",
                    "login": "john_doe-unique",
                    "password": "qwerty123",
                },
                "profile": {
                    "name": "John Doe",
                    "description": "I'm the best guy for your mocks.",
                },
            }),
        )

    assert exc_info.value.response.status_code == 400
    assert exc_info.value.response.json() == {
        "action": "create account",
        "description": "Account already exists.",
        "details": "There is another account with same value for one of the unique fields.",
    }
