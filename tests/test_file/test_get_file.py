from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_one_file",
    "minio": "minio_with_one_file",
})
async def test_get_file_returns_200_with_correct_body(f):
    result = await f.client.get(
        "/files/4c8a2c85-0fe3-4ab0-b683-96bb1805d370",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 200
    assert result.content == b"image binary data"
    assert result.headers["content-type"] == "image/png"
    assert result.headers["content-length"] == "17"


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_one_account_and_one_session",
    "minio": "minio_with_one_file",
})
async def test_get_file_returns_with_nonexistent_file_returns_404_with_correct_body(f):
    result = await f.client.get(
        "/files/4c8a2c85-0fe3-4ab0-b683-96bb1805d370",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 404
    assert result.json() == {
        "resource": "File",
        "description": "Requested resource not found.",
        "details": "Requested resource doesn't exist or has been deleted.",
    }
