from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.file.types import FileSize
from wlss.profile.types import ProfileName
from wlss.shared.types import Id

from src.account.models import Account
from src.auth.models import Session
from src.config import CONFIG
from src.file.enums import Extension, MimeType
from src.file.models import File
from src.profile.models import Profile
from src.shared.datetime import DATETIME_FORMAT


@pytest.fixture
async def db_with_one_profile_and_one_file(db_empty):
    session = db_empty

    account = Account(
        id=Id(1),
        email=AccountEmail("john.doe@mail.com"),
        login=AccountLogin("john_doe"),
    )
    session.add(account)
    await session.flush()

    auth_session = Session(
        id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"),
        account_id=Id(1),
    )
    session.add(auth_session)
    await session.flush()

    profile = Profile(
        account_id=Id(1),
        avatar_id=None,
        description=None,
        name=ProfileName("John Doe"),
    )
    session.add(profile)
    await session.flush()

    file = File(
        id=UUID("2b41c87b-6f06-438b-9933-2a1568cc593b"),
        extension=Extension.PNG,
        mime_type=MimeType.IMAGE_PNG,
        name="image.png",
        size=FileSize(42),
    )
    session.add(file)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def access_token():
    payload = {
        "account_id": 1,
        "expires_at": (
            (
                datetime.now(tz=timezone.utc) + timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
