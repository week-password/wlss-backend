from __future__ import annotations

from datetime import datetime, timedelta, timezone
from io import BytesIO
from uuid import UUID

import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.file.types import FileName, FileSize
from wlss.profile.types import ProfileDescription, ProfileName
from wlss.shared.types import Id, UtcDatetime
from wlss.wish.types import WishDescription, WishTitle

from api.file.enums import Extension, MimeType
from src.account.models import Account
from src.file.models import File
from src.profile.models import Profile
from src.shared.datetime import utcnow
from src.wish.models import Wish


@pytest.fixture
async def db_with_some_unused_files(db_empty):
    session = db_empty
    session.add_all([
        Account(
            id=Id(1),
            email=AccountEmail("john_doe@mail.com"),
            login=AccountLogin("john_doe"),
        ),
        Profile(
            account_id=Id(1),
            avatar_id=UUID("94d9c227-9cfa-4f2d-af8a-43914347bcaa"),
            name=ProfileName("John Doe"),
            description=ProfileDescription("John Doe's profile description."),
        ),
        File(  # this file is used in Profile.avatar_id and shouldn't be deleted
            id=UUID("94d9c227-9cfa-4f2d-af8a-43914347bcaa"),
            name=FileName("john_doe.png"),
            extension=Extension.PNG,
            mime_type=MimeType.IMAGE_PNG,
            size=FileSize(17),
        ),

        Wish(
            account_id=Id(1),
            avatar_id=UUID("8dd3d697-ac59-45a4-b3f4-e3e7b83f5ca4"),
            title=WishTitle("Horse"),
            description=WishDescription("Horse wish description."),
        ),
        File(  # this file is used in Wish.avatar_id and shouldn't be deleted
            id=UUID("8dd3d697-ac59-45a4-b3f4-e3e7b83f5ca4"),
            name=FileName("horse.png"),
            extension=Extension.PNG,
            mime_type=MimeType.IMAGE_PNG,
            size=FileSize(17),
        ),

        File(  # this file isn't used anywhere but created less than hour ago, so it shouldn't be deleted
            id=UUID("602aec00-1051-4b55-8a28-fb42311f7494"),
            name=FileName("horse.png"),
            extension=Extension.PNG,
            mime_type=MimeType.IMAGE_PNG,
            size=FileSize(17),
            created_at=utcnow(),
        ),

        File(  # this file isn't used anywhere and created more than hour ago, so it should be deleted
            id=UUID("7271d982-3ad2-4479-b6fd-bfe1f48aba1b"),
            name=FileName("horse.png"),
            extension=Extension.PNG,
            mime_type=MimeType.IMAGE_PNG,
            size=FileSize(17),
            created_at=UtcDatetime(datetime.now(tz=timezone.utc) - timedelta(hours=2)),
        ),
    ])

    await session.commit()
    return session


@pytest.fixture
def minio_with_some_unused_files(minio_empty):
    minio = minio_empty

    # this file is used in Profile.avatar_id and shouldn't be deleted
    minio.put_object("files", "94d9c227-9cfa-4f2d-af8a-43914347bcaa", data=BytesIO(b"image binary data"), length=17)

    # this file is used in Wish.avatar_id and shouldn't be deleted
    minio.put_object("files", "8dd3d697-ac59-45a4-b3f4-e3e7b83f5ca4", data=BytesIO(b"image binary data"), length=17)

    # this file isn't used anywhere but created less than hour ago, so it shouldn't be deleted
    minio.put_object("files", "602aec00-1051-4b55-8a28-fb42311f7494", data=BytesIO(b"image binary data"), length=17)

    # this file isn't used anywhere and created more than hour ago, so it should be deleted
    minio.put_object("files", "7271d982-3ad2-4479-b6fd-bfe1f48aba1b", data=BytesIO(b"image binary data"), length=17)
    return minio
