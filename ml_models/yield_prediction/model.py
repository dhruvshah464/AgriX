from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class YieldPredictorMeta:
    model_name: str
    features: list[str]
    score: float
