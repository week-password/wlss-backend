from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, File, UploadFile
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from api.file.constants import EOF_BYTE, MAX_SIZE, MEGABYTE
from api.file.dtos import CreateFileRequest
from src.file.exceptions import FileTooLarge


if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from typing import BinaryIO


async def get_tmp_dir() -> Path:
    return Path(tempfile.mkdtemp())


async def get_new_file(
    file_request: Annotated[UploadFile, File(..., alias="file", validation_alias="file")],
    tmp_dir: Annotated[Path, Depends(get_tmp_dir)],
) -> AsyncIterator[CreateFileRequest]:
    filename = Path(file_request.filename or "")
    extension = filename.suffix.lstrip(".").lower()

    file_path = Path(tmp_dir) / filename
    size = _download_file(file_path, file_request.file)

    try:
        yield CreateFileRequest(
            extension=extension,
            mime_type=file_request.content_type,
            name=str(filename),
            size=size,
            tmp_file_path=file_path,
        )
    except ValidationError as e:
        raise RequestValidationError(e.errors()) from None


def _download_file(dst_path: Path, file_data: BinaryIO) -> int:
    with dst_path.open("wb") as f:
        size = 0
        chunk_data = None
        while chunk_data != EOF_BYTE:  # pylint: disable=while-used
            chunk_data = file_data.read(10 * MEGABYTE)
            chunk_size = f.write(chunk_data)

            size += chunk_size
            if size > MAX_SIZE:
                raise FileTooLarge()
    return size
