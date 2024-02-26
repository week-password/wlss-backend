from __future__ import annotations

import typing
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, delete, ForeignKey, Integer, select, String, UniqueConstraint, update
from sqlalchemy.orm import Mapped, mapped_column

from src.file.models import File
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncSession

    from src.wish.schemas import WishUpdate


class Wish(Base):

    __tablename__ = "wish"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    avatar_id: Mapped[UUID | None] = mapped_column(ForeignKey("file.id"), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    description: Mapped[str | None] = mapped_column(String(10_000), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    async def update(self: Self, session: AsyncSession, wish_update: WishUpdate) -> Wish:
        query = (
            update(Wish)
            .where(Wish.id == self.id)
            .values(
                avatar_id=wish_update.avatar_id,
                description=wish_update.description,
                title=wish_update.title,
            )
            .returning(Wish)
        )
        row = (await session.execute(query)).one()
        return typing.cast(Wish, row.Wish)

    async def delete(self: Self, session: AsyncSession) -> None:
        avatar_id = self.avatar_id

        query = delete(Wish).where(Wish.id == self.id)
        await session.execute(query)
        await session.flush()

        if avatar_id is None:
            return

        query = delete(File).where(File.id == avatar_id)
        await session.execute(query)
        await session.flush()

    async def create_booking(self: Self, session: AsyncSession, account_id: int) -> WishBooking:
        wish_booking = WishBooking(account_id=account_id, wish_id=self.id)
        session.add(wish_booking)
        await session.flush()
        return wish_booking


class WishBooking(Base):

    __tablename__ = "wish_booking"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )
    wish_id: Mapped[int] = mapped_column(ForeignKey("wish.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("account_id", "wish_id", name="account_id__wish_id__unique_together"),
    )

    @classmethod
    async def find_by_wish_ids(cls: type[WishBooking], session: AsyncSession, wish_ids: list[int]) -> list[WishBooking]:
        query = select(WishBooking).where(WishBooking.wish_id.in_(wish_ids))
        rows = (await session.execute(query)).all()
        return [typing.cast(WishBooking, row.WishBooking) for row in rows]

    async def delete(self: Self, session: AsyncSession) -> None:
        query = delete(WishBooking).where(WishBooking.id == self.id)
        (await session.execute(query))
        await session.flush()
