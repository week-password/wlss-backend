from __future__ import annotations

import typing
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, select, text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from wlss.file.types import FileName, FileSize
from wlss.shared.types import UtcDatetime

from api.file.enums import Extension, MimeType
from src.file import exceptions
from src.file.columns import FileNameColumn, FileSizeColumn
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
    name: Mapped[FileName] = mapped_column(FileNameColumn, nullable=False)
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

    @classmethod
    async def is_already_in_use(cls: type[File], session: AsyncSession, file_id: uuid.UUID | None) -> bool:
        if file_id is None:
            return False

        query = text("""
            SELECT
                conrelid::regclass AS referencing_table,
                a.attname AS foreign_key_column
            FROM
                pg_constraint AS c
            JOIN
                pg_attribute AS a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
            WHERE
                confrelid = 'public.file'::regclass
            ;
        """)
        rows = (await session.execute(query)).all()

        subqueries = []
        for table_name, column_name in rows:
            subqueries.append(
                f"""
                    (
                        SELECT
                            {table_name}.{column_name} AS file_id
                        FROM
                            {table_name}
                        WHERE
                            {table_name}.{column_name} = :current_file_id
                    )
                """,
            )
        query = text(" UNION ALL ".join(subqueries))
        rows = (await session.execute(query, params={"current_file_id": file_id})).all()
        return len(rows) > 0  # pylint: disable=compare-to-zero
