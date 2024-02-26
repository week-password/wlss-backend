from __future__ import annotations

import typing
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, update
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.profile import schemas
    from src.profile.schemas import NewProfile


class Profile(Base):

    __tablename__ = "profile"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)

    avatar_id: Mapped[UUID | None] = mapped_column(ForeignKey("file.id"), unique=True)
    description: Mapped[str | None] = mapped_column(String(1000))
    name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    @staticmethod
    async def create(session: AsyncSession, profile_data: NewProfile, account_id: int) -> Profile:
        """Create new profile object."""
        profile = Profile(**profile_data.model_dump(), account_id=account_id)
        session.add(profile)
        await session.flush()
        return profile

    async def update(self: Self, session: AsyncSession, profile_update: schemas.ProfileUpdate) -> Profile:
        query = (
            update(Profile)
            .where(Profile.account_id == self.account_id)
            .values(
                avatar_id=profile_update.avatar_id,
                description=profile_update.description,
                name=profile_update.name,
            )
            .returning(Profile)
        )
        row = (await session.execute(query)).one()
        return typing.cast(Profile, row.Profile)
