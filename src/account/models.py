from __future__ import annotations

import typing
from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import delete, ForeignKey, LargeBinary, select
from sqlalchemy.orm import Mapped, mapped_column
from wlss.account.types import AccountEmail, AccountLogin
from wlss.shared.types import Id, UtcDatetime

from src.account.columns import AccountEmailColumn, AccountLoginColumn
from src.account.exceptions import AccountNotFoundError, DuplicateAccountException
from src.auth.exceptions import SessionNotFoundError
from src.auth.models import Session
from src.friendship.models import Friendship, FriendshipRequest
from src.profile.models import Profile
from src.shared.columns import IdColumn, UtcDatetimeColumn
from src.shared.database import Base
from src.shared.datetime import utcnow
from src.wish.exceptions import WishNotFoundError
from src.wish.models import Wish, WishBooking


if TYPE_CHECKING:
    from typing import Self
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession
    from wlss.account.types import AccountPassword

    from src.account.schemas import NewAccount
    from src.auth import schemas as auth_schemas
    from src.wish import schemas


class Account(Base):

    __tablename__ = "account"

    id: Mapped[Id] = mapped_column(IdColumn, primary_key=True)  # noqa: A003

    created_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False)
    email: Mapped[AccountEmail] = mapped_column(AccountEmailColumn, nullable=False, unique=True)
    login: Mapped[AccountLogin] = mapped_column(AccountLoginColumn, nullable=False, unique=True)
    updated_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False, onupdate=utcnow)

    @staticmethod
    async def create(session: AsyncSession, account_data: NewAccount) -> Account:
        query = select(Account).where(Account.email == account_data.email)
        account_with_same_email = (await session.execute(query)).first()
        if account_with_same_email is not None:
            raise DuplicateAccountException()

        query = select(Account).where(Account.login == account_data.login)
        account_with_same_login = (await session.execute(query)).first()
        if account_with_same_login is not None:
            raise DuplicateAccountException()

        account = Account(
            email=account_data.email,
            login=account_data.login,
        )
        session.add(account)
        await session.flush()
        return account

    @classmethod
    async def get(cls: type[Account], session: AsyncSession, account_id: Id) -> Account:
        query = select(Account).where(Account.id == account_id)
        row = (await session.execute(query)).one_or_none()
        if row is None:
            raise AccountNotFoundError()
        return typing.cast(Account, row.Account)

    @classmethod
    async def get_by_login(cls: type[Account], session: AsyncSession, login: AccountLogin) -> Account:
        query = select(Account).where(Account.login == login)
        row = (await session.execute(query)).first()
        if row is None:
            raise AccountNotFoundError()
        return typing.cast(Account, row.Account)

    @classmethod
    async def get_by_email(cls: type[Account], session: AsyncSession, email: AccountEmail) -> Account:
        query = select(Account).where(Account.email == email)
        row = (await session.execute(query)).first()
        if row is None:
            raise AccountNotFoundError()
        return typing.cast(Account, row.Account)

    @classmethod
    async def get_by_credentials(
        cls: type[Account],
        session: AsyncSession,
        credentials: auth_schemas.Credentials,
    ) -> Account:
        query = select(Account).where((Account.email == credentials.email) | (Account.login == credentials.login))
        row = (await session.execute(query)).one_or_none()
        if row is None:
            raise AccountNotFoundError()
        account: Account = row.Account
        # pylint: disable-next=protected-access
        password_hash = await account._get_password_hash(session)  # noqa: SLF001
        await password_hash.check_password(credentials.password)
        return typing.cast(Account, row.Account)

    async def create_session(self: Self, session: AsyncSession) -> Session:
        auth_session = Session(account_id=self.id)
        session.add(auth_session)
        await session.flush()
        return auth_session

    async def _get_password_hash(self: Self, session: AsyncSession) -> PasswordHash:
        query = select(PasswordHash).where(PasswordHash.account_id == self.id)
        row = (await session.execute(query)).one()
        return typing.cast(PasswordHash, row.PasswordHash)

    async def has_session(self: Self, session: AsyncSession, session_id: UUID) -> bool:
        query = select(Session).where((Session.id == session_id) & (Session.account_id == self.id))
        row = (await session.execute(query)).one_or_none()
        return row is not None

    async def get_session(self: Self, session: AsyncSession, session_id: UUID) -> Session:
        query = select(Session).where((Session.id == session_id) & (Session.account_id == self.id))
        row = (await session.execute(query)).one_or_none()
        if not row:
            raise SessionNotFoundError()
        return typing.cast(Session, row.Session)

    async def delete_all_sessions(self: Self, session: AsyncSession) -> None:
        query = delete(Session).where(Session.account_id == self.id)
        await session.execute(query)
        await session.flush()

    async def get_profile(self: Self, session: AsyncSession) -> Profile:
        query = select(Profile).where(Profile.account_id == self.id)
        row = (await session.execute(query)).one()
        return typing.cast(Profile, row.Profile)

    async def get_friendships(self: Self, session: AsyncSession) -> list[Friendship]:
        query = select(Friendship).where(Friendship.account_id == self.id)
        rows = (await session.execute(query)).all()
        return [typing.cast(Friendship, row.Friendship) for row in rows]

    async def delete_friendships(self: Self, session: AsyncSession, friend_id: Id) -> None:
        query = (
            delete(Friendship)
            .where(
                (
                    (Friendship.account_id == self.id) & (Friendship.friend_id == friend_id)
                ) | (
                    (Friendship.account_id == friend_id) & (Friendship.friend_id == self.id)
                ),
            )
        )
        await session.execute(query)

    async def get_friendship_requests(self: Self, session: AsyncSession) -> list[FriendshipRequest]:
        query = (
            select(FriendshipRequest)
            .where((FriendshipRequest.sender_id == self.id) | (FriendshipRequest.receiver_id == self.id))
        )
        rows = (await session.execute(query)).all()
        return [typing.cast(FriendshipRequest, row.FriendshipRequest) for row in rows]

    async def create_wish(self: Self, session: AsyncSession, new_wish: schemas.NewWish) -> Wish:
        wish = Wish(
            account_id=self.id,
            avatar_id=new_wish.avatar_id,
            description=new_wish.description,
            title=new_wish.title,
        )
        session.add(wish)
        await session.flush()
        return wish

    async def get_wish(self: Self, session: AsyncSession, wish_id: Id) -> Wish:
        query = select(Wish).where((Wish.id == wish_id) & (Wish.account_id == self.id))
        row = (await session.execute(query)).one_or_none()
        if row is None:
            raise WishNotFoundError()
        return typing.cast(Wish, row.Wish)

    async def get_wishes(self: Self, session: AsyncSession) -> list[Wish]:
        query = select(Wish).where(Wish.account_id == self.id)
        rows = (await session.execute(query)).all()
        return [typing.cast(Wish, row.Wish) for row in rows]

    async def get_wish_bookings(self: Self, session: AsyncSession) -> list[WishBooking]:
        query = (
            select(WishBooking)
            .join(Wish, Wish.id == WishBooking.wish_id)
            .where(Wish.account_id == self.id)
        )
        rows = (await session.execute(query)).all()
        return [typing.cast(WishBooking, row.WishBooking) for row in rows]

    async def has_friend(self: Self, session: AsyncSession, friend_id: Id) -> bool:
        query = select(Friendship).where((Friendship.account_id == self.id) & (Friendship.friend_id == friend_id))
        row = (await session.execute(query)).one_or_none()
        return row is not None


class PasswordHash(Base):

    __tablename__ = "password_hash"

    account_id: Mapped[Id] = mapped_column(ForeignKey("account.id"), primary_key=True)

    created_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False)
    updated_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False, onupdate=utcnow)
    value: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    @staticmethod
    async def create(session: AsyncSession, password: AccountPassword, account_id: Id) -> PasswordHash:
        hash_value = PasswordHash._generate_hash(password)
        password_hash = PasswordHash(value=hash_value, account_id=account_id)
        session.add(password_hash)
        await session.flush()
        return password_hash

    @staticmethod
    def _generate_hash(password: AccountPassword) -> bytes:
        salt = bcrypt.gensalt()
        byte_password = password.value.encode("utf-8")
        return bcrypt.hashpw(byte_password, salt)

    async def check_password(self: Self, password: AccountPassword) -> None:
        if not bcrypt.checkpw(password.value.encode("utf-8"), self.value):
            raise AccountNotFoundError()
