"""Database models for file."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.file.enums import Extension, MimeType
from src.shared.database import Base, DbEnum
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.file.schemas import NewFile


class File(Base):  # pylint: disable=too-few-public-methods
    """File database model."""

    __tablename__ = "file"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, primary_key=True)  # noqa: A003

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    extension: Mapped[Extension] = mapped_column(DbEnum(Extension), nullable=False)
    mime_type: Mapped[MimeType] = mapped_column(DbEnum(MimeType), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    @staticmethod
    async def create(session: AsyncSession, new_file: NewFile) -> File:
        """Create new file object."""
        file = File(
            extension=new_file.extension,
            mime_type=new_file.mime_type,
            size=new_file.size,
        )
        session.add(file)
        await session.flush()
        return file
