from __future__ import annotations

import typing
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, select, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from wlss.file.types import FileSize
from wlss.shared.types import UtcDatetime

from api.file.enums import Extension, MimeType
from src.file import exceptions
from src.file.columns import FileSizeColumn
from src.shared.columns import UtcDatetimeColumn
from src.shared.database import Base
from src.shared.datetime import utcnow


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.file.schemas import NewFile


class File(Base):

    __tablename__ = "file"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)  # noqa: A003

    created_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False)
    extension: Mapped[Extension] = mapped_column(Enum(Extension, name="extension_enum"), nullable=False)
    mime_type: Mapped[MimeType] = mapped_column(Enum(MimeType, name="mime_type_enum"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[FileSize] = mapped_column(FileSizeColumn, nullable=False)
    updated_at: Mapped[UtcDatetime] = mapped_column(UtcDatetimeColumn, default=utcnow, nullable=False, onupdate=utcnow)

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
