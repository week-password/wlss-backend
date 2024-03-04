from __future__ import annotations

from pathlib import Path

from api.file.enums import Extension, MimeType
from api.file.fields import FileSizeField
from api.shared.schemas import Schema


class NewFile(Schema):

    extension: Extension
    name: str
    mime_type: MimeType
    size: FileSizeField
    tmp_file_path: Path
