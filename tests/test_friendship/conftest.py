from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
import pytest
from wlss.account.types import AccountEmail, AccountLogin
from wlss.profile.types import ProfileName
from wlss.shared.types import Id

from src.account.models import Account
from src.auth.models import Session
from src.config import CONFIG
from src.friendship.enums import FriendshipRequestStatus
from src.friendship.models import Friendship, FriendshipRequest
from src.profile.models import Profile
from src.shared.datetime import DATETIME_FORMAT


@pytest.fixture
async def db_with_two_accounts(db_empty):
    session = db_empty

    accounts = [
        Account(
            id=Id(1),
            email=AccountEmail("john.doe@mail.com"),
            login=AccountLogin("john_doe"),
        ),
        Account(
            id=Id(2),
            email=AccountEmail("john.smith@mail.com"),
            login=AccountLogin("john_smith"),
        ),
    ]
    session.add_all(accounts)
    await session.flush()

    auth_session = Session(
        id=UUID("b9dd3a32-aee8-4a6b-a519-def9ca30c9ec"),
        account_id=Id(1),
    )
    session.add(auth_session)
    await session.flush()

    profiles = [
        Profile(
            account_id=Id(1),
            avatar_id=None,
            description=None,
            name=ProfileName("John Doe"),
        ),
        Profile(
            account_id=Id(2),
            avatar_id=None,
            description=None,
            name=ProfileName("John Smith"),
        ),
    ]
    session.add_all(profiles)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_one_friendship_request(db_with_two_accounts):  # pylint: disable=redefined-outer-name
    session = db_with_two_accounts

    friendship_request = FriendshipRequest(id=Id(1), receiver_id=Id(2), sender_id=Id(1))
    session.add(friendship_request)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_friendship_request_from_another_user(db_with_two_accounts):  # pylint: disable=redefined-outer-name
    session = db_with_two_accounts

    friendship_request = FriendshipRequest(id=Id(1), receiver_id=Id(1), sender_id=Id(2))
    session.add(friendship_request)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_three_accounts_and_three_friendship_requests(
    db_with_two_accounts,  # pylint: disable=redefined-outer-name
):
    session = db_with_two_accounts

    account = Account(
        id=Id(3),
        email=AccountEmail("john.bloggs@mail.com"),
        login=AccountLogin("john_bloggs"),
    )
    session.add(account)
    await session.flush()

    profile = Profile(
        account_id=Id(3),
        avatar_id=None,
        description=None,
        name=ProfileName("John Bloggs"),
    )
    session.add(profile)
    await session.flush()

    friendship_requests = [
        FriendshipRequest(
            sender_id=Id(1),
            receiver_id=Id(2),
            status=FriendshipRequestStatus.PENDING,
        ),
        FriendshipRequest(
            sender_id=Id(2),
            receiver_id=Id(3),
            status=FriendshipRequestStatus.PENDING,
        ),
        FriendshipRequest(
            sender_id=Id(3),
            receiver_id=Id(1),
            status=FriendshipRequestStatus.PENDING,
        ),
    ]
    session.add_all(friendship_requests)
    await session.flush()

    await session.commit()
    return session


@pytest.fixture
async def db_with_two_friendships(db_with_two_accounts):  # pylint: disable=redefined-outer-name
    session = db_with_two_accounts

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
