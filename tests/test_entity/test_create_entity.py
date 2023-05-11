import pytest
from sqlalchemy import select

from src.entity.models import Entity


@pytest.mark.anyio
async def test_create_entity_creates_objects_in_db_correctly(client, db):
    result = await client.post("/entities")

    assert result.status_code == 200
    entities = (await db.execute(select(Entity))).scalars().all()
    assert len(entities)
