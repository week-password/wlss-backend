from __future__ import annotations

from pathlib import Path
from uuid import UUID

from pydantic import Field

from src.file.constants import MEGABYTE
from src.file.enums import Extension, MimeType
from src.shared.schemas import Schema


class File(Schema):
    id: UUID  # noqa: A003

    extension: Extension
    mime_type: MimeType
    size: int = Field(le=10 * MEGABYTE)


class NewFile(Schema):

    extension: Extension
    name: str
    mime_type: MimeType
    size: int = Field(le=10 * MEGABYTE)
    tmp_file_path: Path
