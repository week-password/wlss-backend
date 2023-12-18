"""FastAPI dependencies related to file."""

from __future__ import annotations

import tempfile
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Annotated, BinaryIO

from fastapi import Depends, UploadFile
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.file.constants import EOF_BYTE, MEGABYTE
from src.file.exceptions import FileTooLarge
from src.file.fields import Size
from src.file.schemas import NewFile


async def get_tmp_dir() -> AsyncIterator[Path]:
    """Get temporary directory. FastAPI dependency."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


async def get_new_file(
    upload_file: UploadFile,
    tmp_dir: Annotated[Path, Depends(get_tmp_dir)],
) -> AsyncIterator[NewFile]:
    """Get file info from UploadFile. FastAPI dependency."""
    filename = Path(upload_file.filename or "")
    extension = filename.suffix.lstrip(".").lower()

    file_path = Path(tmp_dir) / filename
    size = _download_file(file_path, upload_file.file)

    try:
        yield NewFile(
            extension=extension,
            file_path=file_path,
            mime_type=upload_file.content_type,
            size=size,
        )
    except ValidationError as e:
        raise RequestValidationError(e.raw_errors) from None


def _download_file(dst_path: Path, file_data: BinaryIO) -> int:
    with dst_path.open("wb") as f:
        size = 0
        chunk_data = None
        while chunk_data != EOF_BYTE:  # pylint: disable=while-used
            chunk_data = file_data.read(10 * MEGABYTE)
            chunk_size = f.write(chunk_data)

            size += chunk_size
            if size > Size.VALUE_MAX:
                raise FileTooLarge()
    return size
