"""Routes for dummy Entity model."""

from __future__ import annotations

import io
from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity import schemas
from src.entity.models import Entity
from src.shared.database import get_session
from src.shared.minio import get_minio, Minio


router = APIRouter()


@router.post("/entities")
async def create_entity(
    entity_body: Annotated[schemas.NewEntity, Body()],
    db: AsyncSession = Depends(get_session),
    minio: Minio = Depends(get_minio),
) -> None:
    """Create entity."""
    new_entity = Entity(**entity_body.dict())
    db.add(new_entity)

    file_content = b"some text"
    minio.put_object(
        bucket_name=new_entity.bucket,
        object_name=new_entity.key,
        data=io.BytesIO(file_content),
        length=len(file_content),
    )

    await db.commit()


@router.get("/entities/{entity_id}")
async def get_entity(entity_id: int, db: AsyncSession = Depends(get_session)) -> schemas.Entity:
    """Get entity."""
    query = select(Entity).where(Entity.id == entity_id)
    entity = (await db.execute(query)).scalar_one()
    return schemas.Entity.from_orm(entity)
