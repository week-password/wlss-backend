from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_with_one_file", "minio": "minio_with_one_file"})
async def test_get_file_returns_200_with_correct_content_and_headers(f):
    result = await f.client.get(
        "/files/2923d1c0-45e8-4ecb-9cae-c3f7b31ed84c",
        headers={"Authorization": "Bearer token"},
    )

    assert result.status_code == 200
    assert result.content == b"image binary data"
    assert result.headers["content-type"] == "image/png"
    assert result.headers["content-length"] == "17"


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_empty", "minio": "minio_empty"})
async def test_get_file_with_nonexistent_file_returns_404_with_correct_body(f):
    result = await f.client.get(
        "/files/2923d1c0-45e8-4ecb-9cae-c3f7b31ed84c",
        headers={"Authorization": "Bearer token"},
    )

    assert result.status_code == 404
    assert result.json() == {
        "resource": "file",
        "description": "Requested file not found.",
        "details": "Requested file doesn't exist or has been deleted.",
    }
