from __future__ import annotations

from pathlib import Path

from src.file.enums import Extension, MimeType
from src.file.fields import FileSizeField
from src.shared.schemas import Schema


class NewFile(Schema):

    extension: Extension
    name: str
    mime_type: MimeType
    size: FileSizeField
    tmp_file_path: Path
