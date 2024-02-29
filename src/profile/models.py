from __future__ import annotations

import typing
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, update
from sqlalchemy.orm import Mapped, mapped_column
from wlss.profile.types import ProfileDescription, ProfileName
from wlss.shared.types import Id, UtcDatetime

from src.profile.columns import ProfileDescriptionColumn, ProfileNameColumn
from src.shared.columns import UtcDatetimeColumn
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.profile import schemas
    from src.profile.schemas import NewProfile


class Profile(Base):

    __tablename__ = "profile"

    account_id: Mapped[Id] = mapped_column(ForeignKey("account.id"), primary_key=True)

    avatar_id: Mapped[UUID | None] = mapped_column(ForeignKey("file.id"), unique=True)
    description: Mapped[ProfileDescription | None] = mapped_column(ProfileDescriptionColumn)
    name: Mapped[ProfileName] = mapped_column(ProfileNameColumn, nullable=False)
    updated_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False, onupdate=utcnow)

    @staticmethod
    async def create(session: AsyncSession, profile_data: NewProfile, account_id: Id) -> Profile:
        """Create new profile object."""
        profile = Profile(
            account_id=account_id,
            description=profile_data.description,
            name=profile_data.name,
        )
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
