"""Entity model."""

from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base


class Entity(Base):  # pylint: disable=too-few-public-methods
    """Dummy model for db testing purposes."""

    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
