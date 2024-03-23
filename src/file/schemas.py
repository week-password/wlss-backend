from __future__ import annotations

from pathlib import Path

from api.file.enums import Extension, MimeType
from api.file.fields import FileNameField, FileSizeField
from api.shared.schemas import Schema


class NewFile(Schema):

    extension: Extension
    name: FileNameField
    mime_type: MimeType
    size: FileSizeField
    tmp_file_path: Path
