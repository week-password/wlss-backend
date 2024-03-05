from __future__ import annotations

import pytest


@pytest.mark.anyio
@pytest.mark.fixtures({
    "access_token": "access_token",
    "client": "client",
    "db": "db_with_three_profiles",
})
async def test_get_profiles_returns_200_with_correct_response(f):
    result = await f.client.get(
        "/profiles?account_id=1&account_id=2",
        headers={"Authorization": f"Bearer {f.access_token}"},
    )

    assert result.status_code == 200
