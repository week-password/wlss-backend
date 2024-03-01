from __future__ import annotations

from unittest.mock import patch

import dirty_equals
import jwt
import pytest
from sqlalchemy import select
from wlss.shared.types import Id

from src.auth.models import Session
from src.config import CONFIG
from src.shared.database import Base
from tests.utils.dirty_equals import IsUtcDatetime, IsUtcDatetimeSerialized
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_create_session_returns_200_with_correct_response(f):
    result = await f.client.post("/sessions", json={"login": "john_doe", "password": "qwerty123"})

    assert result.status_code == 201
    assert result.json() == {
        "session": {
            "id": dirty_equals.IsUUID(4),
            "account_id": 1,
        },
        "tokens": {
            "access_token": dirty_equals.IsStr,
            "refresh_token": dirty_equals.IsStr,
        },
    }
    access_token = result.json()["tokens"]["access_token"]
    assert jwt.decode(access_token, CONFIG.SECRET_KEY, "HS256") == {
        "account_id": 1,
        "expires_at": IsUtcDatetimeSerialized,
        "session_id": dirty_equals.IsUUID(4),
    }
    refresh_token = result.json()["tokens"]["refresh_token"]
    assert jwt.decode(refresh_token, CONFIG.SECRET_KEY, "HS256") == {
        "account_id": 1,
        "expires_at": IsUtcDatetimeSerialized,
        "session_id": dirty_equals.IsUUID(4),
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_create_session_creates_session_in_db_correctly(f):
    result = await f.client.post("/sessions", json={"login": "john_doe", "password": "qwerty123"})  # noqa: F841

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
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_create_session_with_no_login_and_email_provided_returns_422_with_correct_response(f):
    result = await f.client.post("/sessions", json={"password": "qwerty123"})

    assert result.status_code == 422
    assert result.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body"],
                "msg": "Value error, Either 'login' or 'email' is required.",
                "input": {
                    "password": "qwerty123",
                },
                "ctx": {"error": {}},
                "url": "https://errors.pydantic.dev/2.5/v/value_error",
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_create_session_with_both_login_and_email_provided_returns_422_with_correct_response(f):
    result = await f.client.post(
        "/sessions",
        json={"email": "john.doe@mail.com", "login": "john_doe", "password": "qwerty123"},
    )

    assert result.status_code == 422
    assert result.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["body"],
                "msg": "Value error, You cannot use 'login' and 'email' together. Choose one of them.",
                "input": {
                    "email": "john.doe@mail.com",
                    "login": "john_doe",
                    "password": "qwerty123",
                },
                "ctx": {"error": {}},
                "url": "https://errors.pydantic.dev/2.5/v/value_error",
            },
        ],
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_empty"})
async def test_create_session_with_nonexistent_account_returns_404_with_correct_response(f):
    result = await f.client.post("/sessions", json={"login": "john_doe", "password": "qwerty123"})

    assert result.status_code == 404
    assert result.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_create_session_with_wrong_credentials_returns_404_with_correct_response(f):
    result = await f.client.post("/sessions", json={"login": "john_doe", "password": "wrong password"})

    assert result.status_code == 404
    assert result.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
