from __future__ import annotations

import pytest

from api.account.dtos import CreateAccountRequest, CreateAccountResponse
from tests.utils.dirty_equals import IsIdSerialized, IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_empty"})
async def test(f):
    result = await f.api.account.create_account(
        request_data=CreateAccountRequest.model_validate({
            "account": {
                "email": "john.doe@mail.com",
                "login": "john_doe",
                "password": "qwerty123",
            },
            "profile": {
                "name": "John Doe",
                "description": "I'm the best guy for your mocks.",
            },
        }),
    )

    assert isinstance(result, CreateAccountResponse)
    assert result.model_dump() == {
        "account": {
            "id": IsIdSerialized,
            "created_at": IsUtcDatetimeSerialized,
            "email": "john.doe@mail.com",
            "login": "john_doe",
        },
        "profile": {
            "account_id": IsIdSerialized,
            "avatar_id": None,
            "description": "I'm the best guy for your mocks.",
            "name": "John Doe",
        },
    }
