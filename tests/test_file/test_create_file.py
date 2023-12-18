from __future__ import annotations

import uuid
from unittest.mock import patch

import pytest
from sqlalchemy import select

from src.file.enums import Extension, MimeType
from src.file.fields import Size
from src.file.models import File
from src.shared.database import Base
from src.shared.datetime import utcnow
from tests.utils.dirty_equals import UtcDatetime, UUID, UuidStr
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "minio": "minio_empty", "db": "db_empty"})
async def test_create_file_returns_201_with_correct_body(f):
    result = await f.client.post(
        "/files",
        headers={"Authorization": "Bearer token"},
        files={"upload_file": ("image.png", b"image binary data", "image/png")},
    )

    assert result.status_code == 201
    assert result.json() == {
        "id": UuidStr(like="c1f53759-5fd9-41f8-94f0-17b8b77a51e7"),
        "extension": "png",
        "mime_type": "image/png",
        "size": 17,
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "minio": "minio_empty", "db": "db_empty"})
async def test_create_file_creates_objects_in_db_correctly(f):
    result = await f.client.post(  # noqa: F841
        "/files",
        headers={"Authorization": "Bearer token"},
        files={"upload_file": ("image.png", b"image binary data", "image/png")},
    )

    with patch.object(Base, "__eq__", __eq__):
        files = (await f.db.execute(select(File))).scalars().all()
        assert files == [
            File(
                id=UUID(like=uuid.uuid4()),
                created_at=UtcDatetime(like=utcnow()),
                extension=Extension.PNG,
                mime_type=MimeType.IMAGE_PNG,
                size=17,
                updated_at=UtcDatetime(like=utcnow()),
            ),
        ]


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "minio": "minio_empty", "db": "db_empty"})
async def test_create_file_creates_objects_in_minio_correctly(f):
    result = await f.client.post(  # noqa: F841
        "/files",
        headers={"Authorization": "Bearer token"},
        files={"upload_file": ("image.png", b"image binary data", "image/png")},
    )

    objects = list(f.minio.list_objects(bucket_name="files"))
    assert len(objects) == 1
    file_data = f.minio.get_object(bucket_name="files", object_name=objects[0].object_name)
    assert file_data.read() == b"image binary data"
    file_data.release_conn()


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client"})
async def test_create_file_with_too_large_file_returns_413_with_correct_body(f):
    large_image_data = b"x" * (Size.VALUE_MAX + 1)

    result = await f.client.post(
        "/files",
        headers={"Authorization": "Bearer token"},
        files={"upload_file": ("image.png", large_image_data, "image/png")},
    )

    assert result.status_code == 413
    assert result.json() == {
        "resource": "file",
        "description": "File size is too large.",
        "details": "File size is too large and it cannot be handled.",
    }


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client"})
async def test_create_file_with_filename_without_extension_returns_422_with_correct_body(f):
    result = await f.client.post(
        "/files",
        headers={"Authorization": "Bearer token"},
        files={"upload_file": ("image", b"image binary data", "image/png")},
    )

    assert result.status_code == 422
    assert result.json() == {
        "detail": [
            {
                "loc": ["extension"],
                "msg": (
                    "value is not a valid enumeration member; "
                    "permitted: 'gif', 'jfif', 'jif', 'jpe', 'jpeg', 'jpg', 'png', 'webp'"
                ),
                "type": "type_error.enum",
                "ctx": {"enum_values": ["gif", "jfif", "jif", "jpe", "jpeg", "jpg", "png", "webp"]},
            },
        ],
    }
