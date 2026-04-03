from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin, UUIDMixin


class Region(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "regions"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(String(120), nullable=False)
    country: Mapped[str] = mapped_column(String(120), default="India")
    geometry_wkt: Mapped[str | None] = mapped_column(Text, nullable=True)

    farms = relationship("Farm", back_populates="region")
