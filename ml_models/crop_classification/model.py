from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CropClassificationModelMeta:
    model_name: str
    classes: list[str]
    accuracy: float
