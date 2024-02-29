from __future__ import annotations

from unittest.mock import patch

import bcrypt
import pytest
from sqlalchemy import select
from wlss.account.types import AccountEmail, AccountLogin
from wlss.profile.types import ProfileDescription, ProfileName

from src.account.models import Account, PasswordHash
from src.profile.models import Profile
from src.shared.database import Base
from tests.utils.dirty_equals import IsId, IsIdSerialized, IsUtcDatetime, IsUtcDatetimeSerialized
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
                created_at=IsUtcDatetime,
                email=AccountEmail("john.doe@mail.com"),
                id=IsId,
                login=AccountLogin("john_doe"),
                updated_at=IsUtcDatetime,
            ),
        ]
        profiles = (await f.db.execute(select(Profile))).scalars().all()
        assert profiles == [
            Profile(
                account_id=IsId,
                avatar_id=None,
                description=ProfileDescription("I'm the best guy for your mocks."),
                name=ProfileName("John Doe"),
                updated_at=IsUtcDatetime,
            ),
        ]
        password_hashes = (await f.db.execute(select(PasswordHash))).scalars().all()
        assert password_hashes == [
            PasswordHash(
                account_id=IsId,
                created_at=IsUtcDatetime,
                updated_at=IsUtcDatetime,
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
