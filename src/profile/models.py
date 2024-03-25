from __future__ import annotations

import typing
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, select, update
from sqlalchemy.orm import Mapped, mapped_column
from wlss.profile.types import ProfileDescription, ProfileName
from wlss.shared.types import Id, UtcDatetime

from src.file.exceptions import FileAlreadyInUse
from src.file.models import File
from src.profile.columns import ProfileDescriptionColumn, ProfileNameColumn
from src.shared.columns import UtcDatetimeColumn
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.account.models import Account
    from src.profile import schemas
    from src.profile.schemas import NewProfile


class Profile(Base):

    __tablename__ = "profile"

    account_id: Mapped[Id] = mapped_column(ForeignKey("account.id"), primary_key=True)

    avatar_id: Mapped[UUID | None] = mapped_column(ForeignKey("file.id"), unique=True)
    created_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False)
    description: Mapped[ProfileDescription | None] = mapped_column(ProfileDescriptionColumn)
    name: Mapped[ProfileName] = mapped_column(ProfileNameColumn, nullable=False)
    updated_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False, onupdate=utcnow)

    @staticmethod
    async def create(session: AsyncSession, profile_data: NewProfile, account: Account) -> Profile:
        """Create new profile object."""
        profile = Profile(
            account_id=account.id,
            created_at=account.created_at,
            description=profile_data.description,
            name=profile_data.name,
            updated_at=account.updated_at,
        )
        session.add(profile)
        await session.flush()
        return profile

    async def update(self: Self, session: AsyncSession, profile_update: schemas.ProfileUpdate) -> Profile:
        if (
            self.avatar_id != profile_update.avatar_id
            and await File.is_already_in_use(session, profile_update.avatar_id)
        ):
            raise FileAlreadyInUse()

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

    @staticmethod
    async def get_multiple(session: AsyncSession, account_ids: list[Id]) -> list[Profile]:
        query = select(Profile).where(Profile.account_id.in_(account_ids))
        rows = (await session.execute(query)).all()
        return [typing.cast(Profile, row.Profile) for row in rows]

    @staticmethod
    async def search_profiles(session: AsyncSession) -> list[Profile]:
        query = select(Profile).order_by(Profile.created_at.desc())
        rows = (await session.execute(query)).all()
        return [typing.cast(Profile, row.Profile) for row in rows]
