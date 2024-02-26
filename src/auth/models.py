from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, delete, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncSession


class Session(Base):  # pylint: disable=too-few-public-methods

    __tablename__ = "session"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)  # noqa: A003

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    async def delete(self: Self, session: AsyncSession) -> None:
        query = delete(Session).where(Session.id == self.id)
        await session.execute(query)
        await session.flush()
