from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_get_health_returns_correct_response(client):
    result = await client.get("/health")

    assert result.status_code == 200
    assert result.json() == {"status": "OK"}
