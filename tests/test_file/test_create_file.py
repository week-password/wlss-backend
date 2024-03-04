from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import dirty_equals
import httpx
import pytest
from sqlalchemy import select
from wlss.file.types import FileSize

from api.file.dtos import CreateFileRequest, CreateFileResponse
from api.file.enums import Extension, MimeType
from src.file.models import File
from src.shared.database import Base
from tests.utils.dirty_equals import IsUtcDatetime
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_returns_correct_response(f):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = Path(tmp_dir) / "image.png"
        tmp_file_path.write_bytes(b"image binary data")

        result = await f.api.file.create_file(
            token=f.access_token,
            request_data=CreateFileRequest(
                name="image.png",
                mime_type="image/png",
                extension="png",
                size=17,
                tmp_file_path=tmp_file_path,
            ),
        )

    assert isinstance(result, CreateFileResponse)
    assert result.model_dump() == {
        "id": dirty_equals.IsUUID(4),
        "extension": Extension("png"),
        "mime_type": MimeType("image/png"),
        "size": 17,
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_creates_file_in_db_correctly(f):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = Path(tmp_dir) / "image.png"
        tmp_file_path.write_bytes(b"image binary data")

        result = await f.api.file.create_file(  # noqa: F841
            token=f.access_token,
            request_data=CreateFileRequest(
                name="image.png",
                mime_type="image/png",
                extension="png",
                size=17,
                tmp_file_path=tmp_file_path,
            ),
        )

    with patch.object(Base, "__eq__", __eq__):
        files = (await f.db.execute(select(File))).scalars().all()
        assert files == [
            File(
                created_at=IsUtcDatetime,
                id=dirty_equals.IsUUID(4),
                extension=Extension.PNG,
                mime_type=MimeType.IMAGE_PNG,
                name="image.png",
                size=FileSize(17),
                updated_at=IsUtcDatetime,
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_uploads_file_to_minio_correctly(f):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = Path(tmp_dir) / "image.png"
        tmp_file_path.write_bytes(b"image binary data")

        result = await f.api.file.create_file(  # noqa: F841
            token=f.access_token,
            request_data=CreateFileRequest(
                name="image.png",
                mime_type="image/png",
                extension="png",
                size=17,
                tmp_file_path=tmp_file_path,
            ),
        )

    files = list(f.minio.list_objects("files"))
    assert len(files) == 1
    file = files[0]
    assert file.object_name == dirty_equals.IsUUID(4)
    assert file.size == 17
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "file"
        f.minio.fget_object("files", files[0].object_name, file_path)
        assert file_path.read_bytes() == b"image binary data"


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
@patch("src.file.dependencies.MAX_SIZE", 10)  # lower max size to improve test's performance
async def test_create_file_with_too_large_file_raises_correct_exception(f):
    large_image_data = b"x" * 11
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = Path(tmp_dir) / "image.png"
        tmp_file_path.write_bytes(large_image_data)

        with pytest.raises(httpx.HTTPError) as exc_info:
            await f.api.file.create_file(
                token=f.access_token,
                request_data=CreateFileRequest(
                    name="image.png",
                    mime_type="image/png",
                    extension="png",
                    size=17,
                    tmp_file_path=tmp_file_path,
                ),
            )

    assert exc_info.value.response.status_code == 413
    assert exc_info.value.response.json() == {
        "resource": "file",
        "description": "File size is too large.",
        "details": "File size is too large and it cannot be handled.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_with_filename_without_extension_raises_correct_exception(f):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = Path(tmp_dir) / "image.png"
        tmp_file_path.write_bytes(b"image binary data")

        with pytest.raises(httpx.HTTPError) as exc_info:
            await f.api.file.create_file(
                token=f.access_token,
                request_data=CreateFileRequest(
                    name="image",
                    mime_type="image/png",
                    extension="png",
                    size=17,
                    tmp_file_path=tmp_file_path,
                ),
            )

    assert exc_info.value.response.status_code == 422
    assert exc_info.value.response.json() == {
        "detail": [
            {
                "type": "enum",
                "loc": ["extension"],
                "msg": "Input should be 'gif', 'jfif', 'jif', 'jpe', 'jpeg', 'jpg', 'png' or 'webp'",
                "input": "",
                "ctx": {"expected": "'gif', 'jfif', 'jif', 'jpe', 'jpeg', 'jpg', 'png' or 'webp'"},
            },
        ],
    }
