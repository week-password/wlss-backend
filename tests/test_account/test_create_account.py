from __future__ import annotations

from unittest.mock import patch

import bcrypt
import dirty_equals
import pytest
from sqlalchemy import select

from src.account.models import Account, PasswordHash
from src.profile.models import Profile
from src.shared.database import Base
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_empty"})
async def test_create_account_returns_201_with_correct_body(f):
    result = await f.client.post(
        "/accounts",
        json={
            "account": {
                "email": "john.doe@mail.com",
                "login": "john_doe",
                "password": "qwerty123",
            },
            "profile": {
                "name": "John Doe",
                "description": "I'm the best guy for your mocks.",
            },
        },
    )

    assert result.status_code == 201
    assert result.json() == {
        "account": {
            "id": dirty_equals.IsPositiveInt,
            "created_at": dirty_equals.IsDatetime(format_string="%Y-%m-%dT%H:%M:%S.%fZ"),
            "email": "john.doe@mail.com",
            "login": "john_doe",
        },
        "profile": {
            "account_id": dirty_equals.IsPositiveInt,
            "avatar_id": None,
            "description": "I'm the best guy for your mocks.",
            "name": "John Doe",
        },
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_empty"})
async def test_create_account_creates_objects_in_db_correctly(f):
    with (
        patch.object(bcrypt, "hashpw", lambda *_: b"password-hash"),
    ):

        result = await f.client.post(  # noqa: F841
            "/accounts",
            json={
                "account": {
                    "email": "john.doe@mail.com",
                    "login": "john_doe",
                    "password": "qwerty123",
                },
                "profile": {
                    "name": "John Doe",
                    "description": "I'm the best guy for your mocks.",
                },
            },
        )

    with patch.object(Base, "__eq__", __eq__):
        accounts = (await f.db.execute(select(Account))).scalars().all()
        assert accounts == [
            Account(
                created_at=dirty_equals.IsDatetime(enforce_tz=True),
                email="john.doe@mail.com",
                id=dirty_equals.IsPositiveInt,
                login="john_doe",
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
            ),
        ]
        profiles = (await f.db.execute(select(Profile))).scalars().all()
        assert profiles == [
            Profile(
                account_id=dirty_equals.IsPositiveInt,
                avatar_id=None,
                description="I'm the best guy for your mocks.",
                name="John Doe",
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
            ),
        ]
        password_hashes = (await f.db.execute(select(PasswordHash))).scalars().all()
        assert password_hashes == [
            PasswordHash(
                account_id=dirty_equals.IsPositiveInt,
                created_at=dirty_equals.IsDatetime(enforce_tz=True),
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
                value=b"password-hash",
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_create_account_with_already_existed_email_returns_400_with_correct_body(f):
    result = await f.client.post(
        "/accounts",
        json={
            "account": {
                "email": "john.doe@mail.com",
                "login": "john_doe-unique",
                "password": "qwerty123",
            },
            "profile": {
                "name": "John Doe",
                "description": "I'm the best guy for your mocks.",
            },
        },
    )

    assert result.status_code == 400
    assert result.json() == {
        "action": "create account",
        "description": "Account already exists.",
        "details": "There is another account with same value for one of the unique fields.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_account"})
async def test_create_account_with_already_existed_login_returns_400_with_correct_body(f):
    result = await f.client.post(
        "/accounts",
        json={
            "account": {
                "email": "john.doe-unique@mail.com",
                "login": "john_doe",
                "password": "qwerty123",
            },
            "profile": {
                "name": "John Doe",
                "description": "I'm the best guy for your mocks.",
            },
        },
    )

    assert result.status_code == 400
    assert result.json() == {
        "action": "create account",
        "description": "Account already exists.",
        "details": "There is another account with same value for one of the unique fields.",
    }
