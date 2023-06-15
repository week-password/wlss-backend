from __future__ import annotations

import pytest

from src.entity.models import Entity


@pytest.fixture
async def db_with_one_entity(db_empty):
    db = db_empty
    db.add(Entity(id=1, bucket="entity", key="entity-key"))
    await db.commit()
    return db
