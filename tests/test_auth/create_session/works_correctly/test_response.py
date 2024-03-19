from __future__ import annotations

import dirty_equals
import jwt
import pytest

from api.auth.dtos import CreateSessionRequest, CreateSessionResponse
from src.config import CONFIG
from tests.utils.dirty_equals import IsUtcDatetimeSerialized


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test(f):
    result = await f.api.auth.create_session(
        request_data=CreateSessionRequest.model_validate({"login": "john_doe", "password": "qwerty123"}),
    )

    assert isinstance(result, CreateSessionResponse)
    assert result.model_dump() == {
        "session": {
            "id": dirty_equals.IsUUID(4),
            "account_id": 1,
        },
        "tokens": {
            "access_token": dirty_equals.IsStr,
            "refresh_token": dirty_equals.IsStr,
        },
    }
    access_token = result.model_dump()["tokens"]["access_token"]
    assert jwt.decode(access_token, CONFIG.SECRET_KEY, "HS256") == {
        "account_id": 1,
        "created_at": IsUtcDatetimeSerialized,
        "session_id": dirty_equals.IsUUID(4),
    }
    refresh_token = result.model_dump()["tokens"]["refresh_token"]
    assert jwt.decode(refresh_token, CONFIG.SECRET_KEY, "HS256") == {
        "account_id": 1,
        "created_at": IsUtcDatetimeSerialized,
        "session_id": dirty_equals.IsUUID(4),
    }
