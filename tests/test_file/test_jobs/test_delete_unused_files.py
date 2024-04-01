from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

import pytest
from sqlalchemy import select
from wlss.file.types import FileName, FileSize

from api.file.enums import Extension, MimeType
from src.file.jobs import delete_unused_files
from src.file.models import File
from src.shared.database import Base
from tests.utils.dirty_equals import IsUtcDatetime
from tests.utils.mocks.models import __eq__


@pytest.mark.anyio
@pytest.mark.fixtures({"db": "db_with_some_unused_files", "minio": "minio_with_some_unused_files"})
async def test_delete_unused_files_deletes_files_correctly(f):
    await delete_unused_files(f.db)

    files = list(f.minio.list_objects("files"))
    files.sort(key=lambda v: v.object_name)
    assert len(files) == 3

    file = files[0]
    assert file.object_name == "602aec00-1051-4b55-8a28-fb42311f7494"
    assert file.size == 17
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "file"
        f.minio.fget_object("files", files[0].object_name, file_path)
        assert file_path.read_bytes() == b"image binary data"

    file = files[1]
    assert file.object_name == "8dd3d697-ac59-45a4-b3f4-e3e7b83f5ca4"
    assert file.size == 17
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "file"
        f.minio.fget_object("files", files[0].object_name, file_path)
        assert file_path.read_bytes() == b"image binary data"

    file = files[2]
    assert file.object_name == "94d9c227-9cfa-4f2d-af8a-43914347bcaa"
    assert file.size == 17
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "file"
        f.minio.fget_object("files", files[0].object_name, file_path)
        assert file_path.read_bytes() == b"image binary data"

    with patch.object(Base, "__eq__", __eq__):
        files = (await f.db.execute(select(File))).scalars().all()
        assert files == [
            File(  # this file is used in Profile.avatar_id and shouldn't be deleted
                id=UUID("94d9c227-9cfa-4f2d-af8a-43914347bcaa"),
                name=FileName("john_doe.png"),
                extension=Extension.PNG,
                mime_type=MimeType.IMAGE_PNG,
                size=FileSize(17),
                created_at=IsUtcDatetime,
                updated_at=IsUtcDatetime,
            ),
            File(  # this file is used in Wish.avatar_id and shouldn't be deleted
                id=UUID("8dd3d697-ac59-45a4-b3f4-e3e7b83f5ca4"),
                name=FileName("horse.png"),
                extension=Extension.PNG,
                mime_type=MimeType.IMAGE_PNG,
                size=FileSize(17),
                created_at=IsUtcDatetime,
                updated_at=IsUtcDatetime,
            ),

            File(  # this file isn't used anywhere but created less than hour ago, so it shouldn't be deleted
                id=UUID("602aec00-1051-4b55-8a28-fb42311f7494"),
                name=FileName("horse.png"),
                extension=Extension.PNG,
                mime_type=MimeType.IMAGE_PNG,
                size=FileSize(17),
                created_at=IsUtcDatetime,
                updated_at=IsUtcDatetime,
            ),
        ]
