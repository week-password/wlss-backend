import pytest

from src.entity.models import Entity


@pytest.fixture
async def db_with_one_entity(db):
    db.add(Entity(id=1))
    await db.commit()
    return db
