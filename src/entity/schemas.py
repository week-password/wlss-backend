"""Pydantic schemas for Entity dummy model."""

from pydantic.main import BaseModel


class Entity(BaseModel):
    """Entity schema."""

    id: int  # noqa: A003
    bucket: str
    key: str

    class Config:
        """Pydantic's special class to configure pydantic models."""

        orm_mode = True


class NewEntity(BaseModel):
    """New entity schema."""

    bucket: str
    key: str
