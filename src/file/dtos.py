from __future__ import annotations

from pathlib import Path

from fastapi.responses import FileResponse
from pydantic import Field

from src.file.enums import Extension, MimeType
from src.file.fields import FileSizeField
from src.shared.fields import UuidField
from src.shared.schemas import Schema


class CreateFileRequest(Schema):
    extension: Extension = Field(..., example="png")
    name: str = Field(..., example="image.png")
    mime_type: MimeType = Field(..., example="image/png")
    size: FileSizeField = Field(..., example=2048)
    tmp_file_path: Path


class CreateFileResponse(Schema):
    id: UuidField = Field(..., example="47b3d7a9-d7d3-459a-aac1-155997775a0e")  # noqa: A003
    extension: Extension = Field(..., example="png")
    mime_type: MimeType = Field(..., example="image/png")
    size: FileSizeField = Field(..., example=2048)


class GetFileResponse(FileResponse):
    ...
