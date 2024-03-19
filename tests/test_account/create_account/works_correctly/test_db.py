from __future__ import annotations

from unittest.mock import patch

import bcrypt
import pytest
from sqlalchemy import select
from wlss.account.types import AccountEmail, AccountLogin
from wlss.profile.types import ProfileDescription, ProfileName

from api.account.dtos import CreateAccountRequest
from src.account.models import Account, PasswordHash
from src.profile.models import Profile
from src.shared.database import Base
from tests.utils.dirty_equals import IsId, IsUtcDatetime
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"api": "api", "db": "db_empty"})
async def test(f):
    with (
        patch.object(bcrypt, "hashpw", lambda *_: b"password-hash"),
    ):

        result = await f.api.account.create_account(  # noqa: F841
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
