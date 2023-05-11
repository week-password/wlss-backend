"""Routes for dummy Entity model."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity import schemas
from src.entity.models import Entity
from src.shared.database import get_session


router = APIRouter()


@router.post("/entities")
async def create_entity(db: AsyncSession = Depends(get_session)) -> None:
    """Create entity."""
    db.add(Entity())
    await db.commit()


@router.get("/entities/{entity_id}")
async def get_entity(entity_id: int, db: AsyncSession = Depends(get_session)) -> schemas.Entity:
    """Get entity."""
    query = select(Entity).where(Entity.id == entity_id)
    entity = (await db.execute(query)).scalar_one()
    return schemas.Entity.from_orm(entity)
