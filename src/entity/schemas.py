"""Pydantic schemas for Entity dummy model."""

from pydantic.main import BaseModel


class Entity(BaseModel):
    """Entity schema."""

    id: int  # noqa: A003

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic's special class to configure pydantic models."""

        orm_mode = True
