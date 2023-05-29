from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import select

from src.entity.models import Entity


@pytest.mark.anyio
async def test_create_entity_creates_objects_in_db_correctly(client, db):
    result = await client.post("/entities", json={"bucket": "entity", "key": "entity-key"})

    assert result.status_code == 200
    entities = (await db.execute(select(Entity))).scalars().all()
    assert len(entities)


@pytest.mark.anyio
async def test_create_entity_stores_files_in_minio_correctly(client, db, minio, tmp_path):
    tmp_path = Path(tmp_path)

    result = await client.post("/entities", json={"bucket": "entity", "key": "entity-key"})

    assert result.status_code == 200
    entity = (await db.execute(select(Entity))).scalar_one()
    minio.fget_object(entity.bucket, entity.key, tmp_path / "file")
    with (tmp_path / "file").open() as f:
        assert f.read() == "some text"
