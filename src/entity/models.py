"""Entity model."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base


class Entity(Base):  # pylint: disable=too-few-public-methods
    """Dummy model for db testing purposes."""

    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003

    bucket: Mapped[str] = mapped_column(String)
    key: Mapped[str] = mapped_column(String)
