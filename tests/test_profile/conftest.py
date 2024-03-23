from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import jwt
import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.file.types import FileName, FileSize
from wlss.profile.types import ProfileName
from wlss.shared.types import Id

from api.file.enums import Extension, MimeType
from api.shared.datetime import DATETIME_FORMAT
from src.account.models import Account
from src.auth.models import Session
from src.config import CONFIG
from src.file.models import File
from src.profile.models import Profile


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
        name=FileName("image.png"),
        size=FileSize(42),
    )
    session.add(file)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_three_profiles(db_with_one_profile_and_one_file):  # pylint: disable=redefined-outer-name
    session = db_with_one_profile_and_one_file

    session.add_all([
        Account(
            id=Id(2),
            email=AccountEmail("john.smith@mail.com"),
            login=AccountLogin("john_smith"),
        ),
        Profile(
            account_id=Id(2),
            avatar_id=None,
            description=None,
            name=ProfileName("John Smith"),
        ),
        Account(
            id=Id(3),
            email=AccountEmail("john.bloggs@mail.com"),
            login=AccountLogin("john_bloggs"),
        ),
        Profile(
            account_id=Id(3),
            avatar_id=None,
            description=None,
            name=ProfileName("John Bloggs"),
        ),
    ])
    await session.flush()
    return session


@pytest.fixture
async def access_token():
    payload = {
        "account_id": 1,
        "created_at": datetime.now(tz=timezone.utc).strftime(DATETIME_FORMAT),
        "session_id": "b9dd3a32-aee8-4a6b-a519-def9ca30c9ec",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
