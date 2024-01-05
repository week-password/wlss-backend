from __future__ import annotations

import io

import pytest

from src.file.models import File


@pytest.fixture
async def db_with_one_file(db_empty):
    session = db_empty
    file = File(id="2923d1c0-45e8-4ecb-9cae-c3f7b31ed84c", extension="png", mime_type="image/png", size=17)
    session.add(file)
    await session.commit()
    return session


@pytest.fixture
async def minio_with_one_file(minio_empty):
    minio = minio_empty
    minio.put_object("files", "2923d1c0-45e8-4ecb-9cae-c3f7b31ed84c", data=io.BytesIO(b"image binary data"), length=17)
    return minio
