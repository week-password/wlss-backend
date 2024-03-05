from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.file.types import FileSize
from wlss.shared.types import Id
from wlss.wish.types import WishDescription, WishTitle

from src.account.models import Account, PasswordHash
from src.auth.models import Session
from src.config import CONFIG
from src.file.enums import Extension, MimeType
from src.file.models import File
from src.friendship.models import Friendship
from src.shared.datetime import DATETIME_FORMAT
from src.wish.models import Wish, WishBooking
from tests.utils import bcrypt as bcrypt_cached


@pytest.fixture
async def db_with_one_account_and_one_file(db_empty):
    session = db_empty

    account = Account(id=Id(1), email=AccountEmail("john.doe@mail.com"), login=AccountLogin("john_doe"))
    session.add(account)
    await session.flush()

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=account.id, value=hash_value)
    session.add(password_hash)
    await session.flush()

    auth_session = Session(id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"), account_id=Id(1))
    session.add(auth_session)
    await session.flush()

    file = File(
        id=UUID("0b928aaa-521f-47ec-8be5-396650e2a187"),
        extension=Extension.PNG,
        mime_type=MimeType.IMAGE_PNG,
        name="image.png",
        size=FileSize(17),
    )
    session.add(file)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_one_wish(db_with_one_account_and_one_file):  # pylint: disable=redefined-outer-name
    session = db_with_one_account_and_one_file
    wish = Wish(
        id=Id(1),
        account_id=Id(1),
        avatar_id=UUID("0b928aaa-521f-47ec-8be5-396650e2a187"),
        description=WishDescription("I'm gonna take my horse to the old town road."),
        title=WishTitle("Horse"),
    )
    session.add(wish)
    await session.flush()

    return session


@pytest.fixture
async def db_with_one_wish_without_avatar(db_with_one_account_and_one_file):  # pylint: disable=redefined-outer-name
    session = db_with_one_account_and_one_file
    wish = Wish(
        id=Id(1),
        account_id=Id(1),
        avatar_id=None,
        description=WishDescription("I'm gonna take my horse to the old town road."),
        title=WishTitle("Horse"),
    )
    session.add(wish)
    await session.flush()

    return session


@pytest.fixture
async def db_with_two_files_and_one_wish(db_with_one_wish):  # pylint: disable=redefined-outer-name
    session = db_with_one_wish

    file = File(
        id=UUID("4b94605b-f5e1-40b1-b9fc-c635c9529e3e"),
        extension=Extension.PNG,
        mime_type=MimeType.IMAGE_PNG,
        name="new_image.png",
        size=FileSize(17),
    )
    session.add(file)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_two_accounts_and_one_file(db_with_one_account_and_one_file):  # pylint: disable=redefined-outer-name
    session = db_with_one_account_and_one_file

    account = Account(id=Id(2), email=AccountEmail("john.smith@mail.com"), login=AccountLogin("john_smith"))
    session.add(account)
    await session.flush()

    auth_session = Session(id=UUID("a3bdfc12-ad0b-419c-97fa-59695798ca80"), account_id=Id(2))
    session.add(auth_session)
    await session.flush()

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=Id(2), value=hash_value)
    session.add(password_hash)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_two_accounts_and_one_wish(db_with_one_wish):  # pylint: disable=redefined-outer-name
    session = db_with_one_wish

    account = Account(id=Id(2), email=AccountEmail("john.smith@mail.com"), login=AccountLogin("john_smith"))
    session.add(account)
    await session.flush()

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=Id(2), value=hash_value)
    session.add(password_hash)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_two_friend_accounts_and_one_wish(  # pylint: disable=redefined-outer-name
    db_with_two_accounts_and_one_file,
):
    session = db_with_two_accounts_and_one_file

    friendships = [
        Friendship(
            account_id=Id(1),
            friend_id=Id(2),
        ),
        Friendship(
            account_id=Id(2),
            friend_id=Id(1),
        ),
    ]
    session.add_all(friendships)
    await session.flush()

    wish = Wish(
        id=Id(1),
        account_id=Id(2),
        avatar_id=UUID("0b928aaa-521f-47ec-8be5-396650e2a187"),
        description=WishDescription("I'm gonna take my horse to the old town road."),
        title=WishTitle("Horse"),
    )
    session.add(wish)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_two_friend_accounts_and_one_wish_booking(  # pylint: disable=redefined-outer-name
    db_with_two_friend_accounts_and_one_wish,
):
    session = db_with_two_friend_accounts_and_one_wish

    wish_booking = WishBooking(id=Id(1), account_id=Id(1), wish_id=Id(1))
    session.add(wish_booking)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_two_accounts_and_two_wishes(  # pylint: disable=redefined-outer-name
    db_with_two_accounts_and_one_wish,
):
    session = db_with_two_accounts_and_one_wish

    file = File(
        id=UUID("4b94605b-f5e1-40b1-b9fc-c635c9529e3e"),
        extension=Extension.PNG,
        mime_type=MimeType.IMAGE_PNG,
        name="new_image.png",
        size=FileSize(17),
    )
    session.add(file)
    await session.flush()

    wish = Wish(
        id=Id(2),
        account_id=Id(1),
        avatar_id=UUID("4b94605b-f5e1-40b1-b9fc-c635c9529e3e"),
        description=WishDescription("I need some sleep. Time to put the old horse down."),
        title=WishTitle("Sleep"),
    )
    session.add(wish)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_three_friend_accounts_and_one_booking(  # pylint: disable=redefined-outer-name
    db_with_two_friend_accounts_and_one_wish,
):
    session = db_with_two_friend_accounts_and_one_wish

    account = Account(id=Id(3), email=AccountEmail("john.bloggs@mail.com"), login=AccountLogin("john_bloggs"))
    session.add(account)
    await session.flush()

    auth_session = Session(id=UUID("8d0c487d-dd59-4d6a-b102-620633cb33ab"), account_id=Id(3))
    session.add(auth_session)
    await session.flush()

    hash_value = bcrypt_cached.hashpw(b"qwerty123", salt=b"$2b$12$K4wmY3GEMQFoMvpuFK.GMu")
    password_hash = PasswordHash(account_id=Id(3), value=hash_value)
    session.add(password_hash)

    friendships = [
        Friendship(
            account_id=Id(1),
            friend_id=Id(3),
        ),
        Friendship(
            account_id=Id(3),
            friend_id=Id(1),
        ),
    ]
    session.add_all(friendships)
    await session.flush()

    wish_booking = WishBooking(id=Id(1), account_id=Id(1), wish_id=Id(1))
    session.add(wish_booking)
    await session.flush()

    await session.flush()
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


@pytest.fixture
async def access_token_for_another_account():
    payload = {
        "account_id": 3,
        "expires_at": (
            (
                datetime.now(tz=timezone.utc) + timedelta(days=CONFIG.DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION)
            ).strftime(DATETIME_FORMAT)
        ),
        "session_id": "8d0c487d-dd59-4d6a-b102-620633cb33ab",
    }
    return jwt.encode(payload, CONFIG.SECRET_KEY, "HS256")
