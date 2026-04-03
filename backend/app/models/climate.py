from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base, TimestampMixin, UUIDMixin


class ClimateForecast(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "climate_forecasts"

    region_id: Mapped[str] = mapped_column(ForeignKey("regions.id"), nullable=False)
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    rainfall_mm: Mapped[float] = mapped_column(Float, nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=False)
    drought_index: Mapped[float] = mapped_column(Float, nullable=False)
