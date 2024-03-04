from __future__ import annotations

from uuid import UUID

import httpx
import pytest

from api.file.dtos import GetFileResponse


@pytest.mark.anyio
@pytest.mark.fixtures({
    "api": "api",
    "access_token": "access_token",
    "db": "db_with_one_file",
    "minio": "minio_with_one_file",
    "tmp_path": "tmp_path",
})
async def test_get_file_returns_correct_response(f):
    tmp_file_path = f.tmp_path / "image.png"

    result = await f.api.file.get_file(
        file_id=UUID("4c8a2c85-0fe3-4ab0-b683-96bb1805d370"),
        token=f.access_token,
        tmp_file_path=tmp_file_path,
    )

    assert isinstance(result, GetFileResponse)
    assert result.media_type == "image/png"
    assert result.path.read_bytes() == b"image binary data"


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "api": "api",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_with_one_file",
    "tmp_path": "tmp_path",
})
async def test_get_file_returns_with_nonexistent_file_raises_correct_exception(f):
    tmp_file_path = f.tmp_path / "image.png"
    with pytest.raises(httpx.HTTPError) as exc_info:
        await f.api.file.get_file(
            file_id=UUID("4c8a2c85-0fe3-4ab0-b683-96bb1805d370"),
            token=f.access_token,
            tmp_file_path=tmp_file_path,
        )

    assert exc_info.value.response.status_code == 404
    assert exc_info.value.response.json() == {
        "resource": "File",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
