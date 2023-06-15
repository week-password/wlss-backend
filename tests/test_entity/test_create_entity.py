from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import select

from src.entity.models import Entity


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_empty"})
async def test_create_entity_creates_objects_in_db_correctly(f):
    result = await f.client.post("/entities", json={"bucket": "entity", "key": "entity-key"})

    assert result.status_code == 200
    entities = (await f.db.execute(select(Entity))).scalars().all()
    assert len(entities)


@pytest.mark.anyio
@pytest.mark.fixtures({"client": "client", "db": "db_empty", "minio": "minio_empty", "tmp_path": "tmp_path"})
async def test_create_entity_stores_files_in_minio_correctly(f):
    tmp_path = Path(f.tmp_path)

    result = await f.client.post("/entities", json={"bucket": "entity", "key": "entity-key"})

    assert result.status_code == 200
    entity = (await f.db.execute(select(Entity))).scalar_one()
    f.minio.fget_object(entity.bucket, entity.key, tmp_path / "file")
    with (tmp_path / "file").open() as f_:
        assert f_.read() == "some text"
