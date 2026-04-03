"""Backward-compatible schema exports for earlier scaffold."""

from backend.app.schemas.prediction import YieldPredictionRequest, YieldPredictionResponse

__all__ = ["YieldPredictionRequest", "YieldPredictionResponse"]
