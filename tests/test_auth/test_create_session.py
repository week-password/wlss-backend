from __future__ import annotations

import json
from unittest.mock import patch

import dirty_equals
import httpx
import jwt
import pydantic
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from api.auth.dtos import CreateSessionRequest, CreateSessionResponse
from src.auth.models import Session
from src.config import CONFIG
from src.shared.database import Base
from tests.utils.dirty_equals import IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_create_session_returns_correct_response(f):
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


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_create_session_creates_session_in_db_correctly(f):
    result = await f.api.auth.create_session(  # noqa: F841
        request_data=CreateSessionRequest.model_validate({"login": "john_doe", "password": "qwerty123"}),
    )

    with patch.object(Base, "__eq__", __eq__):
        rows = (await f.db.execute(select(Session))).scalars().all()
        assert rows == [
            Session(
                id=dirty_equals.IsUUID(4),
                account_id=Id(1),
                created_at=IsUtcDatetime,
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_create_session_with_no_login_and_email_provided_raises_correct_exception(f):
    with pytest.raises(pydantic.ValidationError) as exc_info:
        await f.api.auth.create_session(request_data=CreateSessionRequest.model_validate({"password": "qwerty123"}))

    assert json.loads(exc_info.value.json()) == [
        {
            "type": "value_error",
            "loc": [],
            "msg": "Value error, Either 'login' or 'email' is required.",
            "input": {"password": "qwerty123"},
            "ctx": {"error": "Either 'login' or 'email' is required."},
            "url": "https://errors.pydantic.dev/2.5/v/value_error",
        },
    ]


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_create_session_with_both_login_and_email_provided_raises_correct_exception(f):
    with pytest.raises(pydantic.ValidationError) as exc_info:
        await f.api.auth.create_session(
            request_data=CreateSessionRequest.model_validate({
                "email": "john.doe@mail.com",
                "login": "john_doe",
                "password": "qwerty123",
            }),
        )

    assert json.loads(exc_info.value.json()) == [
        {
            "type": "value_error",
            "loc": [],
            "msg": "Value error, You cannot use 'login' and 'email' together. Choose one of them.",
            "input": {
                "email": "john.doe@mail.com",
                "login": "john_doe",
                "password": "qwerty123",
            },
            "ctx": {
                "error": "You cannot use 'login' and 'email' together. Choose one of them.",
            },
            "url": "https://errors.pydantic.dev/2.5/v/value_error",
        },
    ]


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_empty"})
async def test_create_session_with_nonexistent_account_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.auth.create_session(
            request_data=CreateSessionRequest.model_validate({"login": "john_doe", "password": "qwerty123"}),
        )

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_with_one_account"})
async def test_create_session_with_wrong_credentials_raises_correct_exception(f):
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.auth.create_session(
            request_data=CreateSessionRequest.model_validate({"login": "john_doe", "password": "wrong password"}),
        )

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
