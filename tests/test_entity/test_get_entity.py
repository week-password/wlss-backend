from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_get_entity_returns_200_with_correct_body(client, db_with_one_entity):
    result = await client.get("/entities/1")

    assert result.status_code == 200
    assert result.json() == {"id": 1, "bucket": "entity", "key": "entity-key"}
