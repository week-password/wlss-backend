"""Schemas for file related functionality."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from src.file.enums import Extension, MimeType
from src.file.fields import Size
from src.shared.schemas import Schema


class NewFile(Schema):
    """File data which is going to be created."""

    extension: Extension
    file_path: Path
    mime_type: MimeType
    size: Size


class File(Schema):
    """File schema."""

    id: UUID  # noqa: A003

    extension: Extension
    mime_type: MimeType
    size: Size

    class Config:
        """Pydantic's special class to configure pydantic models."""

        orm_mode = True
