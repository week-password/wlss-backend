from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base


class Instance(Base):

    __tablename__ = "instance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String)


class FloatingIP(Base):

    __tablename__ = "floating_ip"

    ip: Mapped[str] = mapped_column(String, primary_key=True)
    role: Mapped[str] = mapped_column(String)
