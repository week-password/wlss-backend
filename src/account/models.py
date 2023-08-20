"""Database models for account."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import DateTime, ForeignKey, Integer, LargeBinary, select, String
from sqlalchemy.orm import Mapped, mapped_column

from src.account.exceptions import DuplicateAccountException
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.auth.fields import Password
    from src.auth.schemas import NewAccount


class Account(Base):  # pylint: disable=too-few-public-methods
    """Account database model."""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    login: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    @staticmethod
    async def create(session: AsyncSession, account_data: NewAccount) -> Account:
        """Create new account object."""
        query = select(Account).where(Account.email == account_data.email)
        account_with_same_email = (await session.execute(query)).first()
        if account_with_same_email is not None:
            raise DuplicateAccountException()

        query = select(Account).where(Account.login == account_data.login)
        account_with_same_login = (await session.execute(query)).first()
        if account_with_same_login is not None:
            raise DuplicateAccountException()

        account = Account(**account_data.dict(exclude={"password"}))
        session.add(account)
        await session.flush()
        return account


class PasswordHash(Base):  # pylint: disable=too-few-public-methods
    """Password hash database model."""

    __tablename__ = "password_hash"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), autoincrement=False, primary_key=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )
    value: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    @staticmethod
    async def create(session: AsyncSession, password: Password, account_id: int) -> PasswordHash:
        """Create a password hash object."""
        hash_value = PasswordHash._generate_hash(password)
        password_hash = PasswordHash(value=hash_value, account_id=account_id)
        session.add(password_hash)
        await session.flush()
        return password_hash

    @staticmethod
    def _generate_hash(password: Password) -> bytes:
        """Generate hash for password."""
        salt = bcrypt.gensalt()
        raw_password = password.get_secret_value()
        byte_password = raw_password.encode("utf-8")
        return bcrypt.hashpw(byte_password, salt)
