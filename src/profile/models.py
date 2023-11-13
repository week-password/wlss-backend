"""Database models for profile."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.auth.schemas import NewProfile


class Profile(Base):  # pylint: disable=too-few-public-methods
    """Profile database model."""

    __tablename__ = "profile"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), autoincrement=False, primary_key=True)

    avatar_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), unique=True)
    description: Mapped[String | None] = mapped_column(String)
    name: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    @staticmethod
    async def create(session: AsyncSession, profile_data: NewProfile, account_id: int) -> Profile:
        """Create new profile object."""
        profile = Profile(**profile_data.dict(), account_id=account_id)
        session.add(profile)
        await session.flush()
        return profile
