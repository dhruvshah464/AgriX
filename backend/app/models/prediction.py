from __future__ import annotations

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base, TimestampMixin, UUIDMixin


class YieldPrediction(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "yield_predictions"

    farm_id: Mapped[str] = mapped_column(ForeignKey("farms.id"), nullable=False)
    season: Mapped[str] = mapped_column(String(40), nullable=False)
    model_name: Mapped[str] = mapped_column(String(80), nullable=False)
    predicted_yield_tph: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
