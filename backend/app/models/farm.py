from __future__ import annotations

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, TimestampMixin, UUIDMixin


class Farm(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "farms"

    farmer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    region_id: Mapped[str] = mapped_column(ForeignKey("regions.id"), nullable=False)
    area_hectares: Mapped[float] = mapped_column(Float, nullable=False)
    soil_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    region = relationship("Region", back_populates="farms")
