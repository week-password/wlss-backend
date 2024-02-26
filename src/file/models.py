from __future__ import annotations

import typing
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Integer, select, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.file import exceptions
from src.file.enums import Extension, MimeType
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.file.schemas import NewFile


class File(Base):

    __tablename__ = "file"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)  # noqa: A003

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    extension: Mapped[Extension] = mapped_column(Enum(Extension, name="extension_enum"), nullable=False)
    mime_type: Mapped[MimeType] = mapped_column(Enum(MimeType, name="mime_type_enum"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False, onupdate=utcnow,
    )

    @classmethod
    async def create_file(cls: type[File], session: AsyncSession, new_file: NewFile) -> File:
        file = File(
            extension=new_file.extension,
            mime_type=new_file.mime_type,
            name=new_file.name,
            size=new_file.size,
        )
        session.add(file)
        await session.flush()
        return file

    @classmethod
    async def get(cls: type[File], session: AsyncSession, file_id: uuid.UUID) -> File:
        query = select(File).where(File.id == file_id)
        row = (await session.execute(query)).one_or_none()
        if row is None:
            raise exceptions.FileNotFoundError()
        return typing.cast(File, row.File)
