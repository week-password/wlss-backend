from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import dirty_equals
import pytest
from sqlalchemy import select

from src.file.enums import Extension, MimeType
from src.file.models import File
from src.shared.database import Base
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_returns_201_with_correct_response(f):
    result = await f.client.post(
        "/files",
        headers={"Authorization": f"Bearer {f.access_token}"},
        files={"upload_file": ("image.png", b"image binary data", "image/png")},
    )

    assert result.status_code == 201
    assert result.json() == {
        "id": dirty_equals.IsUUID(4),
        "extension": "png",
        "mime_type": "image/png",
        "size": 17,
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_creates_file_in_db_correctly(f):
    result = await f.client.post(  # noqa: F841
        "/files",
        headers={"Authorization": f"Bearer {f.access_token}"},
        files={"upload_file": ("image.png", b"image binary data", "image/png")},
    )

    with patch.object(Base, "__eq__", __eq__):
        files = (await f.db.execute(select(File))).scalars().all()
        assert files == [
            File(
                created_at=dirty_equals.IsDatetime(enforce_tz=True),
                id=dirty_equals.IsUUID(4),
                extension=Extension.PNG,
                mime_type=MimeType.IMAGE_PNG,
                name="image.png",
                size=17,
                updated_at=dirty_equals.IsDatetime(enforce_tz=True),
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_uploads_file_to_db_correctly(f):
    result = await f.client.post(  # noqa: F841
        "/files",
        headers={"Authorization": f"Bearer {f.access_token}"},
        files={"upload_file": ("image.png", b"image binary data", "image/png")},
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
    "client": "client",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
@patch("src.file.dependencies.MAX_SIZE", 10)  # lower max size to improve test's performance
async def test_create_file_with_too_large_file_returns_413_with_correct_body(f):
    large_image_data = b"x" * 11

    result = await f.client.post(
        "/files",
        headers={"Authorization": f"Bearer {f.access_token}"},
        files={"upload_file": ("image.png", large_image_data, "image/png")},
    )

    assert result.status_code == 413
    assert result.json() == {
        "resource": "file",
        "description": "File size is too large.",
        "details": "File size is too large and it cannot be handled.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_empty",
})
async def test_create_file_with_filename_without_extension_returns_422_with_correct_body(f):
    result = await f.client.post(
        "/files",
        headers={"Authorization": f"Bearer {f.access_token}"},
        files={"upload_file": ("image", b"image binary data", "image/png")},
    )

    assert result.status_code == 422
    assert result.json() == {
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
